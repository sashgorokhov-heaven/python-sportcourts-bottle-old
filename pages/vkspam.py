import bottle
import pages
import config
from modules import vk, logging
import dbutils
import json
import time


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)

def response(obj) -> str:
    return dump({'response':obj})

def error(obj) -> str:
    return dump({'error':obj})

class Error(Exception):
    def __init__(self, code:int, description:str, e:Exception=None, data:dict=None):
        self.code = code
        self.description = description
        self.e=e
        self.data = data
        super().__init__(code, description, e)

    @staticmethod
    def unhandled(e:Exception):
        return Error(0, 'Unhandled exception', e)

    @staticmethod
    def auth_error(login:str, e:Exception):
        return Error(1, 'Auth error for <{}>'.format(login), e)

    @staticmethod
    def no_tokens():
        return Error(2, 'No tokens found')

    @staticmethod
    def vk_error(e:vk.VKError):
        return Error(3, '{}: {}'.format(e.error_dict['error_msg'], e.error_dict['error_msg']), data=e.error_dict)

    @staticmethod
    def template_not_found(name:str):
        return Error(4, 'Template not found:{}'.format(name))

    @staticmethod
    def user_not_found(user_id:int):
        return Error(5, 'User not found:{}'.format(user_id))

    @staticmethod
    def already_sent(user_id:int, spam_type:int):
        return Error(6, 'Already sent user <{}> spam <{}>'.format(user_id, spam_type))

    def json(self) -> dict:
        ret = {'code':self.code, 'description':self.description}
        if self.e:
            ret['eclass'] = self.e.__class__.__name__
            ret['eargs'] = ','.join(list(map(str,self.e.args))) if len(self.e.args)>0 else ''
        if self.data:
            ret['data'] = self.data
        return ret

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return response(func(*args, **kwargs))
        except Error as e:
            return error(e.json())
        except Exception as e:
            logging.error(e)
            return error(Error.unhandled(e).json())
    return wrapper


connection = dbutils.default_connection.copy()
connection['host'] = 'test.sportcourts.ru'
connection['db'] = 'vkbot'


@pages.post('/admin/new_vk/auth')
@pages.only_ajax
@pages.only_admins
def auth():
    with dbutils.dbopen(**connection) as db:
        db.execute("TRUNCATE auth_sessions;")
        accounts = db.execute("SELECT * FROM accounts", ['login', 'password'])
        errors = list()
        success = list()
        for account in accounts:
            try:
                access_token, user_id, expires = vk.auth(account['login'], account['password'], config.vkspam.app_id, config.vkspam.scope)
            except Exception as e:
                errors.append((account['login'], e))
            else:
                db.execute("INSERT INTO auth_sessions (login, access_token) VALUES ('{}', '{}')".format(account['login'], access_token))
                success.append(account['login'])
        errors = [{'login':e[0], 'error':Error.auth_error(*e).json()} for e in errors]
        if len(success)>0:
            if len(errors)==0:
                return response({'success':success})
            else:
                return response({'success':success, 'errors':errors})
        else:
            return error({'errors':errors})


@pages.post('/admin/new_vk/auth/check')
@pages.only_ajax
@pages.only_admins
@handle_error
def check():
    with dbutils.dbopen(**connection) as db:
        db.execute("SELECT login, datetime FROM auth_sessions", ['login', 'datetime'])
        return {i['login']:str(i['datetime'])  for i in db.last()}


@pages.post('/admin/new_vk/users/get/<sport_type:int>')
@pages.only_ajax
@pages.only_admins
@handle_error
def get_users(sport_type:int):
    with dbutils.dbopen(**connection) as db:
        db.execute("SELECT user_id, spam_type, datetime, lasttime FROM users WHERE sport_type={}".format(sport_type),
                   ['user_id', 'spam_type', 'datetime', 'lasttime'])
        return {i['user_id']:{'spam_type':i['spam_type'], 'datetime':str(i['datetime']), 'lasttime':str(i['lasttime'])} for i in db.last()}


users = {'users':set(), 'timestamp':0}

@pages.post('/admin/new_vk/users/send/<user_id:int>/<template_name>/<spam_type:int>')
@pages.only_ajax
@pages.only_admins
@handle_error
def send_message(user_id:int, template_name:str, spam_type:int):
    t = time.time()
    if user_id in users['users']: return {'continued':user_id}
    if t-users['timestamp']>300:
        with dbutils.dbopen() as db:
            db.execute("SELECT DISTINCT vkuserid FROM users WHERE vkuserid!=0")
            users['users'] = set(map(lambda x: x[0], db.last()))
            users['timestamp'] = t
    if user_id in users['users']: return {'continued':user_id}
    with dbutils.dbopen(**connection) as db:
        db.execute("SELECT login, last FROM auth_sessions")
        if len(db.last())==0: raise Error.no_tokens()
        last = min(db.last(), key=lambda x: x[1])[1]
        account = db.execute("SELECT login, access_token, datetime FROM auth_sessions WHERE last={}".format(last),
                   ['login', 'access_token', 'datetime'])[0]
        db.execute("SELECT spam_type FROM users WHERE user_id={}".format(user_id))
        if len(db.last())==0: raise Error.user_not_found(user_id)
        if db.last()[0][0]==spam_type: raise Error.already_sent(user_id, spam_type)
        try:
            vkuser = vk.exec(account['access_token'], "users.get", user_id=user_id)[0]
            message = bottle.template(template_name, first_name=vkuser['first_name'])
            vk.exec(account['access_token'], "messages.send", user_id=user_id, message=message)
        except vk.VKError as e:
            raise Error.vk_error(e)
        except bottle.HTTPError:
            raise Error.template_not_found(template_name)

        db.execute("UPDATE users SET lasttime=NOW(), spam_type={} WHERE user_id={}".format(spam_type, user_id))
        db.execute("UPDATE auth_sessions SET last=last+1 WHERE last={}".format(last))
        account.pop('access_token')
        account['datetime'] = str(account['datetime'])
        return {'account':account, 'time':time.time()-t}