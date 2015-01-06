import bottle
import pages
import config
from modules import vk, logging, utils
import os
import time
import json

_time_format_ = '%Y-%m-%d %H:%M:%S'


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