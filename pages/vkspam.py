import bottle
import pages
import config
from modules import vk, logging, utils
import dbutils
import os
import time
import json

_time_format_ = '%Y-%m-%d %H:%M:%S'


connection = dbutils.default_connection
connection['host'] = 'test.sportcourts.ru'
connection['db'] = 'vkbot'


status = 0
data = None


# 0 - стоит
# 1 - входит
# -1 - нет токенов


@utils.spool("vkmassauth")
def get_access() -> list:
    global data, status
    status = 1
    if not os.path.exists("actk"):
        with open('actk', 'w') as f:
            tokens = dict()
            for account in config.vkspam.accounts:
                try:
                    access_token, user_id, expires = vk.auth(account[0], account[1], config.vkspam.app_id, config.vkspam.scope)
                except Exception as e:
                    logging.message('Error while logging in with VK <{}:{}>'.format(*account), e)
                    continue
                tokens[account[0]] = (access_token, user_id, expires, time.strftime(_time_format_))
            if len(tokens)==0:
                status = -1
                f.write(json.dumps(tokens, ensure_ascii=False))
                data = [i[0] for i in tokens.items()]
                return
            f.write(json.dumps(tokens, ensure_ascii=False))
            data = [i[0] for i in tokens.items()]
            status = 2
            return
    tokens = json.load(open('actc', 'r'))
    for account in config.vkspam.accounts:
        if account[0] not in tokens or int(time.time()) - int(time.mktime(time.strptime(tokens[account[0]][-1], _time_format_))) >= tokens[account[0]][2]:
            try:
                access_token, user_id, expires = vk.auth(account[0], account[1], config.vkspam.app_id, config.vkspam.scope)
            except Exception as e:
                logging.message('Error auth with VK <{}:{}>'.format(*account), e)
                continue
            tokens[account[0]] = (access_token, user_id, expires, time.strftime(_time_format_))
    if len(tokens)==0:
        status = -1
        json.dump(tokens, open('actc', 'w'))
        data = [i[0] for i in tokens.items()]
        return
    json.dump(tokens, open('actc', 'w'))
    data = [i[0] for i in tokens.items()]
    status = 2


@pages.get('/admin/vk')
@pages.only_admins
def auth():
    global status, data
    if status==0 or status==1:
        get_access()
        return 'Выполняется вход. Обождите...'
    elif status==-1:
        if 'reload' not in bottle.request.query:
            return 'Ошибка входа. Добавьте параметр ?reload чтобы попробывать войти снова'
        status = 0
        raise bottle.redirect('/admin/vk')
    return 'Вошел'


accounts = dict()
account_list = list()
last_account = 0

@pages.get('/admin/bad_vk/auth')
@pages.only_ajax
@pages.only_admins
def bad_auth():
    for account in config.vkspam.accounts:
        try:
            access_token, user_id, expires = vk.auth(account[0], account[1], config.vkspam.app_id, config.vkspam.scope)
        except Exception as e:
            logging.message("Error auth <{}>".format(account[0]), e)
            continue
        accounts[account[0]] = access_token
    if len(accounts)>0:
        global account_list
        account_list = list(accounts.keys())
        return {'success':account_list}
    return json.dumps({'Error':'no tokens'})


#@pages.get('/admin/bad_vk/check')
#@pages.only_ajax
#@pages.only_admins
#def bad_check():
#    pass


@pages.get('/admin/bad_vk/get_users/<sport_id:int>')
@pages.only_ajax
@pages.only_admins
def get_users(sport_id:int):
    with dbutils.dbopen(**connection) as db:
        db.execute("SELECT user_id FROM users WHERE sport_type={} AND spam_type=0".format(sport_id))
        users = list(map(lambda x: x[0], db.last()))
        return json.dumps({'users':users})


def get_next_token() -> str:
    global last_account
    last_account += 1
    if last_account==len(account_list):
        last_account = 0
    account = account_list[last_account]
    token = accounts[account]
    return account, token


@pages.get('/admin/bad_vk/send/<user_id:int>/<template>/<spam_type:int>')
@pages.only_ajax
@pages.only_admins
def bad_send(user_id:int, template:str, spam_type:int):
    account, token = get_next_token()
    try:
        vkuser = vk.exec(token, "users.get", user_id=user_id)[0]
        message = bottle.template(template, first_name=vkuser['first_name'])
        vk.exec(token, "messages.send", user_id=user_id, message=message)
        with dbutils.dbopen(**connection) as db:
            db.execute("UPDATE users SET spam_type={} WHERE user_id={}".format(spam_type, user_id))
    except Exception as e:
        logging.message('Error sending message to <{}>: {}'.format(user_id, template), e)
        return json.dumps({'account':account, 'result':'error', 'error':e.__class__.__name__})
    return json.dumps({'account':account, 'result':'success'})