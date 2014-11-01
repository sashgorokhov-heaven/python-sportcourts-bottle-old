import bottle

import dbutils
from models import activation, users, notifications
import pages


class Activate(pages.Page):
    def get(self, **params):
        raise bottle.HTTPError(404) # TODO
        #token = bottle.request.query.get('token')
        #if not token:
        #    raise bottle.HTTPError(404)
        #with dbutils.dbopen() as db:
        #    try:
        #        user_id = activation.get_userid_by_token(token, dbconnection=db)
        #    except ValueError:
        #        return pages.PageBuilder('text', message='Пользователь вроде бы уже активирован.')
        #    activation.activate(user_id, dbconnection=db)
        #    user = users.get(user_id, dbconnection=db)
        #    pages.auth.login(user.email(), user.passwd())
        #    notifications.add(user_id, "Ваш профиль успешно активирован!")
        #    raise bottle.redirect('/profile')

    get.route = '/activate'