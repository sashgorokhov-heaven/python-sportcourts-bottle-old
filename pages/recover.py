import bottle

import pages
from modules import utils, dbutils


class Recover(pages.Page):
    def get(self):
        if pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        return pages.PageBuilder('recover')

    def post(self):
        if pages.auth_dispatcher.loggedin() or 'email' not in bottle.request.forms:
            raise bottle.HTTPError(404)
        email = bottle.request.forms.get('email')
        with dbutils.dbopen() as db:
            db.execute("SELECT user_id, passwd FROM users WHERE email='{}'".format(email))
            if len(db.last()) == 0:
                return pages.PageBuilder('/auth', error='Неверный email.',
                                         error_description='Пользователь с таким email не найден.')
            utils.sendmail('Ваш пароль: {}'.format(db.last()[0][1]), email, 'Восстановление пароля')
            utils.write_notification(db.last()[0][0], 'Вы недавно восстанавливливали пароль', 1)
            return pages.PageBuilder('auth', error='Проверьте email',
                                     error_description='Вам было отправлено письмо с дальнейшими инструкциями.')


    get.route = '/recover'
    post.route = get.route