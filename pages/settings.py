import json

import bottle

import dbutils
import pages
from models import users


class Settings(pages.Page):
    def execute(self, method:str, **kwargs):
        if not pages.auth.loggedin():
            raise bottle.HTTPError(404)
        return super().execute(method, **kwargs)

    def get(self):
        return pages.PageBuilder("settings")

    def post(self):
        with dbutils.dbopen() as db:
            send_email = 'email_notify' in bottle.request.forms
            show_phone = 'all' if 'phone_all' in bottle.request.forms else 'organizers'
            db.execute("UPDATE users SET settings='{}' WHERE user_id={}".format(json.dumps({'send_mail':send_email, 'show_phone':show_phone}), pages.auth.current().user_id()))
            user = users.get(pages.auth.current().user_id(), dbconnection=db)
            pages.auth.reloaduser(user) # TODO: FIX
            raise bottle.redirect("/profile")

    get.route = '/settings'
    post.route = '/settings'