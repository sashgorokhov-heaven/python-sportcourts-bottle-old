import bottle

import dbutils
import pages
from models import notifications, mailing, activation, users


class Recover(pages.Page):
    def get(self):
        if pages.auth.loggedin():
            raise bottle.redirect('/profile')
        return pages.PageBuilder('recover')

    def post(self):
        if pages.auth.loggedin() or 'email' not in bottle.request.forms:
            raise bottle.HTTPError(404)
        email = bottle.request.forms.get('email')
        with dbutils.dbopen() as db:
            db.execute("SELECT user_id, passwd FROM users WHERE email='{}'".format(email))
            if len(db.last()) == 0:
                return pages.PageBuilder('text', message='Неверный email',
                                         description='Пользователь с таким email не найден.')
            user_id = db.last()[0][0]
            passwd = db.last()[0][1]
            mailing.send_to_user(
                user_id,
                'Ваш пароль: {}'.format(passwd),
                'Восстановление пароля',
                override=True,
                dbconnection=db)
            notifications.add(user_id, 'Вы недавно восстанавливливали пароль', 1)
            return pages.PageBuilder('text', message='Проверьте email',
                                     description='Вам было отправлено письмо с дальнейшими инструкциями.')


    get.route = '/recover'
    post.route = get.route