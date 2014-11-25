import bottle
import time

import dbutils
from modules import vk
import pages


@pages.get('/logout')
def logout():
    pages.auth.logout()
    raise bottle.redirect(bottle.request.get_header("Referer", "/"))


def get_code():
    code = bottle.request.query.code
    try:
        access_token, user_id, email = vk.auth_code(code, '/auth')
    except ValueError as e:
        return pages.PageBuilder('auth', error=e.vkerror['error'], error_description=e.vkerror['error_description'])
    with dbutils.dbopen() as db:
        db.execute("SELECT email, passwd FROM users WHERE vkuserid='{}'".format(user_id))
        if not email or len(db.last()) == 0:
            return pages.PageBuilder('auth', error='Ошибка авторизации', error_description="Пользователь не найден.")
        email = db.last()[0][0]
        password = db.last()[0][1]
        try:
            pages.auth.login(email, password)
        except ValueError:
            time.sleep(3)
            return pages.PageBuilder('auth', error='Ошибка авторизации',
                                     error_description='Неверный email или пароль')
        raise bottle.redirect('/games')


@pages.get('/auth')
def get():
    if pages.auth.loggedin():
        raise bottle.redirect('/profile')
    if 'code' in bottle.request.query:
        return get_code()
    return pages.PageBuilder('auth')


@pages.post('/auth')
def post():
    if pages.auth.loggedin():
        raise bottle.redirect('/profile')
    email = bottle.request.forms.email
    password = bottle.request.forms.password
    try:
        pages.auth.login(email, password)
    except ValueError:
        return pages.PageBuilder('auth', email=email, error='Ошибка авторизации',
                                 error_description='Неверный email или пароль')
    return bottle.redirect('/games')