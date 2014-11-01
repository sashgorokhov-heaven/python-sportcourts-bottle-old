import bottle

import config
import dbutils
from modules import vk
import pages


class Authorize(pages.Page):
    def get(self):
        if pages.auth.loggedin():
            raise bottle.redirect('/profile')
        if 'code' in bottle.request.query:
            return self.get_code()
        return pages.PageBuilder('auth')

    def get_code(self):
        code = bottle.request.query.code
        try:
            access_token, user_id, email = vk.auth_code(code, '/auth')
        except ValueError as e:
            return pages.PageBuilder('auth', error=e.vkerror['error'], error_description=e.vkerror['error_description'])

        with dbutils.dbopen() as db:
            db.execute("SELECT passwd FROM users WHERE email='{}'".format(email))
            if len(db.last()) == 0:
                raise bottle.redirect(
                    "https://oauth.vk.com/authorize?client_id=4436558&scope=&redirect_uri=http://{}:{}/registration&response_type=code&v=5.21".format(
                        config.server.ip, config.server.port))
            password = db.last()[0][0]
            try:
                pages.auth.login(email, password)
            except ValueError:
                return pages.PageBuilder('auth', error='Ошибка авторизации',
                                         error_description='Неверный email или пароль')
            raise bottle.redirect(bottle.request.get_header("Referer", "/games"))

    def post(self):
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

    get.route = '/auth'
    post.route = get.route