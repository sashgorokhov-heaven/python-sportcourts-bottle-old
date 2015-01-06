import bottle
import datetime
import time
import itertools
import random
import pages
import dbutils
import json
from modules import logging
from models import users, cities, ampluas, decode_set


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

    @staticmethod
    def restricted_fields(fields:list):
        return Error(5, 'Restricted fields:{}'.format(','.join(fields)))

#    @staticmethod
#    def invalid_field(fields:list):
#        return Error(6, 'Invalid fields:{}'.format(','.join(fields)))

    def json(self) -> dict:
        ret = {'code':self.code, 'description':self.description}
        if self.e:
            ret['eclass'] = self.e.__class__.__name__
            ret['eargs'] = '{}'.format(','.join(list(map(str,self.e.args)))) if len(self.e.args)>0 else ''
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
                if datetime.datetime.now()-au[0]['datetime']>datetime.timedelta(days=7):
                    raise Error.invalid_token()
                return func(*args, **kwargs)
            raise Error.invalid_token()
    return required_param('token')(wrapper)


def strdatetime(d:dict) -> dict:
    for key in d:
        if isinstance(d[key], (datetime.datetime, datetime.date, datetime.time)):
            d[key] = str(d[key])
    return d


def current_user(db:dbutils.DBConnection, detalized:bool=False) -> users.User:
    token = bottle.request.query.get('token')
    user_id = db.execute("SELECT user_id FROM api_auth WHERE token='{}'".format(token))[0][0]
    if detalized:
        return users.get(user_id, dbconnection=db)
    return user_id


_available_fields = {
    "users_get": {
        "restricted": {'email', 'passwd', 'settings', 'referer'}
    },
    "courts_get": {
        "restricted": {'cost', 'phone', 'admin_description'}
    },
    "games_get": {
        "restricted": {'notificated'}
    }
}


def check_fields_access(fields:list, key:str, db:dbutils.DBConnection):
    fields = set(fields)
    f = _available_fields[key]
    user = current_user(db, True)
    if 'available' in f:
        f = f['available']
        if not fields.issubset(f) and not user.userlevel.admin():
            r = set(f).difference_update(f)
            raise Error.restricted_fields(r)
    elif 'restricted' in f:
        f = f['restricted']
        if not fields.isdisjoint(f) and not user.userlevel.admin():
            r = set(fields).intersection(f)
            raise Error.restricted_fields(r)


class getters:
    @staticmethod
    def city(city_id:int, db:dbutils.DBConnection) -> dict:
        city = cities.get(city_id, dbconnection=db)
        return {"city_id": city.city_id(), "title": city.title(), "geopoint": city.geopoint()}

    @staticmethod
    def court(court_id:int, db:dbutils.DBConnection) -> dict:
        pass


@pages.get(['/api/users/get', '/api/users/get/<user_id:int>'])
@handle_error
@check_auth
def users_get(user_id:int=0):
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else '*'
    fields = fields.split(',')

    with dbutils.dbopen() as db:
        this = current_user(db, True)
        if len(fields)==1 and fields[0]=='*':
            fields = dbutils.dbfields['users']
            if not this.userlevel.admin() and (user_id!=0 and user_id!=this.user_id()):
                fields = list(set(fields).difference_update(_available_fields['users_get']['restricted']))
        if user_id==0 or (user_id!=0 and user_id!=this.user_id()):
            check_fields_access(fields, 'users_get', db)
        users_ = db.execute("SELECT {} FROM users{}".format(
            ', '.join(fields),
            ' WHERE user_id={}'.format(user_id) if user_id!=0 else ''),
                            fields)
        list(map(strdatetime, users_))
        for user in users_:
            if 'city_id' in user:
                city = cities.get(user['city_id'], dbconnection=db)
                user['city'] = {
                    "city_id": city.city_id(),
                    "title": city.title(),
                    "geopoint": city.geopoint()}
            if 'ampluas' in user:
                amplua = ampluas.get(decode_set(user['ampluas']), dbconnection=db)
                user['ampluas'] = [{"amplua_id":a.amplua_id(), "sport_type":a.sport_type(), "title":a.title()} for a in amplua]
            if 'settings' in user:
                user['settings'] = json.loads(user['settings'])
        return dump({'count':len(users_), 'users':users_})


@pages.get('/api/courts/get')
@handle_error
@check_auth
def courts_get():
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else 'court_id'
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        this = current_user(db, True)
        if len(fields)==1 and fields[0]=='*':
            fields = dbutils.dbfields['courts']
            if not this.userlevel.admin():
                fields = list(set(fields).difference_update(_available_fields['courts_get']['restricted']))
        check_fields_access(fields, 'courts_get', db)
        courts = db.execute("SELECT {} FROM courts".format(', '.join(fields)), fields)
        list(map(strdatetime, courts))
        return dump({'count':len(courts), 'courts':courts})


@pages.get('/api/games/get')
@handle_error
@check_auth
def games_get():
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else 'game_id'
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        this = current_user(db, True)
        if len(fields)==1 and fields[0]=='*':
            fields = dbutils.dbfields['courts']
            if not this.userlevel.admin():
                fields = list(set(fields).difference_update(_available_fields['courts_get']['restricted']))
        check_fields_access(fields, 'courts_get', db)
        games = db.execute("SELECT {} FROM games".format(', '.join(fields)), fields)
        list(map(strdatetime, games))
        for game in games:
            if 'city_id' in game:
                city = cities.get(game['city_id'], dbconnection=db)
                game['city'] = {
                    "city_id": city.city_id(),
                    "title": city.title(),
                    "geopoint": city.geopoint()}
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