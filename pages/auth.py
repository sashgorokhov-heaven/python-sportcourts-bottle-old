import urllib.request

import bottle

import modules
from modules import dbutils
import pages


class Authorize(pages.Page):
    def get(self):
        if pages.auth_dispatcher.loggedin():
            raise bottle.redirect('/profile')
        if 'code' in bottle.request.query:
            return self.get_code()
        return pages.PageBuilder('auth')

    def get_code(self):
        code = bottle.request.query.code
        url = "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri=http://{3}:{4}/auth"
        url = url.format(modules.config['api']['vk']['appid'],
                         modules.config['api']['vk']['secret'], code,
                         modules.config['server']['ip'], modules.config['server']['port'])
        response = urllib.request.urlopen(url)
        response = response.read().decode()
        response = bottle.json_loads(response)
        if 'error' in response:
            return pages.PageBuilder('auth', error=response['error'], error_description=response['error_description'])
        access_token, user_id, email = response['access_token'], response['user_id'], response.get('email')
        with dbutils.dbopen() as db:
            db.execute("SELECT passwd FROM users WHERE email='{}'".format(email))
            if len(db.last()) == 0:
                raise bottle.redirect(
                    "https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://sportcourts.ru:80/registration&response_type=code&v=5.21")
            password = db.last()[0][0]
            try:
                pages.auth_dispatcher.login(email, password)
            except ValueError:
                return pages.PageBuilder('auth', error='Ошибка авторизации', error_description='Чтото не так')
            raise bottle.redirect('/profile')

    def post(self):
        email = bottle.request.forms.email
        password = bottle.request.forms.password
        try:
            pages.auth_dispatcher.login(email, password)
        except ValueError:
            return pages.PageBuilder('auth', email=email, error='Ошибка авторизации',
                                     error_description='Неправильный email или пароль')
        return bottle.redirect('/profile')

    get.route = '/auth'
    post.route = get.route