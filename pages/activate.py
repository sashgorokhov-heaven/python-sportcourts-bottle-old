import bottle

from modules import dbutils, utils
import pages


class Activate(pages.Page):
    def get(self, **params):
        token = bottle.request.query.get('token')
        if not token:
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            db.execute("SELECT user_id FROM activation WHERE token='{}'".format(token))
            if len(db.last()) == 0:
                raise bottle.HTTPError(404)
            user_id = db.last()[0][0]
            db.execute("UPDATE users SET activated={} WHERE user_id={}".format(1, user_id))
            db.execute("DELETE FROM activation WHERE user_id={}".format(user_id))
            db.execute("SELECT email, passwd FROM users WHERE user_id={}".format(user_id))
            pages.auth_dispatcher.login(*db.last()[0])
            utils.write_notification(user_id, "Ваш профиль успешно активирован!")
            raise bottle.redirect('/profile')

    get.route = '/activate'