import bottle
import pages
from models import settings


class Settings(pages.Page):
    def get(self):
        if not pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        return pages.PageBuilder("settings", settings=settings.get(pages.auth_dispatcher.getuserid()))

    get.route = '/settings'