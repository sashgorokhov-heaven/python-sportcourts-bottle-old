import bottle
import datetime
import time
import itertools
import random
import pages
import dbutils
import json
from modules import logging


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def generate_token() -> str:
    return ''.join(random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))), 20))


class Error(Exception):
    def __init__(self, code:int, description:str, e:Exception=None):
        self.code = code
        self.description = description
        self.e=e
        super().__init__(code, description, e)

    @staticmethod
    def unhandled(e:Exception):
        return Error(0, 'Unhandled exception', e)

    @staticmethod
    def lost_parameter(params:set):
        return Error(1, 'Lost parameters:{}'.format(','.join(params)))

    @staticmethod
    def invalid_auth():
        return Error(2, 'Invalid email or password')

    @staticmethod
    def invalid_token():
        return Error(3, 'Invalid token or token expired')

    @staticmethod
    def invalid_ip(ip:str):
        return Error(4, 'Invalid ip {}'.format(ip))

    def json(self) -> dict:
        ret = {'code':self.code, 'description':self.description}
        if self.e:
            ret['eclass'] = self.e.__class__.__name__
            ret['eargs'] = '<{}>'.format(','.join(self.e.args)) if len(self.e.args)>0 else ''
        return ret


def required_param(*args):
    def decor(func):
        def wrapper(*args2, **kwargs2):
            d = set(args).difference({i for i in bottle.request.query})
            if len(d)>0:
                raise Error.lost_parameter(d)
            return func(*args2, **kwargs2)
        return wrapper
    return decor


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Error as e:
            return dump(e.json())
        except Exception as e:
            logging.error(e)
            return dump(Error.unhandled(e).json())
    return wrapper


def check_auth(func):
    def wrapper(*args, **kwargs):
        token = bottle.request.query.get('token')
        with dbutils.dbopen() as db:
            au = db.execute("SELECT * FROM api_auth WHERE token='{}'".format(token), dbutils.dbfields['api_auth'])
            if len(au)>0:
                if bottle.request.remote_addr!=au[0]['ip']:
                    raise Error.invalid_ip(bottle.request.remote_addr)
                if datetime.datetime.now()-au[0]['datetime']>datetime.timedelta(days=1):
                    raise Error.invalid_token()
                return func(*args, **kwargs)
            raise Error.invalid_token()
    return required_param('token')(wrapper)


def strdatetime(d:dict) -> dict:
    for key in d:
        if isinstance(d[key], (datetime.datetime, datetime.date, datetime.time)):
            d[key] = str(d[key])
    return d


@pages.get('/api/users/get')
@handle_error
@check_auth
def users_get():
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else 'user_id'
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        users = db.execute("SELECT {} FROM users".format(', '.join(fields)), fields)
        list(map(strdatetime, users))
        return dump({'count':len(users), 'users':users})


@pages.get('/api/courts/get')
@handle_error
@check_auth
def courts_get():
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else 'court_id'
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        courts = db.execute("SELECT {} FROM courts".format(', '.join(fields)), fields)
        list(map(strdatetime, courts))
        return dump({'count':len(courts), 'courts':courts})


@pages.get('/api/games/get')
@handle_error
@check_auth
def courts_get():
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else 'game_id'
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        games = db.execute("SELECT {} FROM games".format(', '.join(fields)), fields)
        list(map(strdatetime, games))
        return dump({'count':len(games), 'games':games})


@pages.get('/api/auth')
@handle_error
@required_param('email', 'password')
def auth():
    email = bottle.request.query.get('email')
    passwd = bottle.request.query.get('password')
    ip = bottle.request.remote_addr
    with dbutils.dbopen() as db:
        db.execute("SELECT user_id FROM users WHERE email='{}' AND passwd='{}'".format(email, passwd))
        if len(db.last())==0:
            raise Error.invalid_auth()
        user_id = db.last()[0][0]
        au = db.execute("SELECT * FROM api_auth WHERE user_id={}".format(user_id))
        token = generate_token()
        while True:
            db.execute("SELECT * FROM api_auth WHERE token='{}'".format(token))
            if len(db.last())>0:
                token = generate_token()
                continue
            if len(au)>0:
                db.execute("UPDATE api_auth SET token='{}', datetime=NOW(), ip='{}' WHERE user_id={} ".format(token, ip, user_id))
            else:
                db.execute("INSERT INTO api_auth VALUES ('{}', '{}', NOW(), {}, '{}')".format(token, email, user_id, ip))
            break
        time.sleep(1.5)
        return dump({'token':token, 'user_id':user_id})