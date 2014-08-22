import bottle

import pages
import modules.dbutils


class Authorize(pages.Page):
    path = ['auth']

    def execute(self, method:str):
        if method == 'POST':
            data = self.post()
            if isinstance(data, pages.Template):
                return data.template()
            return data
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    def get(self):
        if pages.loggedin():
            return bottle.redirect('/profile')
        return bottle.template('auth')

    def post(self):
        email = bottle.request.forms.email
        password = bottle.request.forms.password
        with modules.dbutils.dbopen() as db:
            db.execute(
                "SELECT user_id, admin, activated, user_type FROM users WHERE email='{}' AND passwd='{}'".format(email,
                                                                                                                 password),
                ['user_id', 'admin', 'activated', 'user_type'])
            if len(db.last()) == 0:
                return pages.Template('auth', email=email, error='Ошибка авторизации',
                                      error_description='Неправильный email или пароль')
            bottle.response.set_cookie('user_id', db.last()[0]['user_id'], modules.config['secret'])
            bottle.response.set_cookie('adminlevel', db.last()[0]['admin'], modules.config['secret'])
            bottle.response.set_cookie('activated', db.last()[0]['activated'], modules.config['secret'])
            bottle.response.set_cookie('user_type', db.last()[0]['user_type'], modules.config['secret'])
            db.execute("UPDATE users SET lasttime=NOW() WHERE user_id={}".format(db.last()[0]['user_id']))
            return bottle.redirect('/profile')
