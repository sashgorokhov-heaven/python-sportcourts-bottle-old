import bottle

import uwsgi
import pages
import modules.eventslib


class ServerReload(pages.Page):
    def get(self):
        if not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)
        else:
            modules.eventslib.event_server.stop()
            uwsgi.restart()

    get.route = '/sreload'