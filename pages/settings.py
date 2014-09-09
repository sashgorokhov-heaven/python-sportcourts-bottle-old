import bottle
from modules import dbutils
import pages
from models import settings


class Settings(pages.Page):
    def execute(self, method:str, **kwargs):
        if not pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        return super().execute(method, **kwargs)

    def get(self):
        return pages.PageBuilder("settings", settings=settings.get(pages.auth_dispatcher.getuserid()))

    def post(self):
        with dbutils.dbopen() as db:
            sett = settings.get(pages.auth_dispatcher.getuserid(), dbconnection=db)
            sett.send_email(True if 'email_notify' in bottle.request.forms else False)
            sett.show_phone('all' if 'phone_all' in bottle.request.forms else 'organizers')
            settings.set(pages.auth_dispatcher.getuserid(), sett, dbconnection=db)

    get.route = '/settings'
    post.route = '/settings'