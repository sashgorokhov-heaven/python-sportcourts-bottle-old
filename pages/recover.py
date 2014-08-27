import bottle

import pages


class Recover(pages.Page):
    def get(self):
        if pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)

        if 'code' in bottle.request.query:
            pass
        else:
            raise bottle.HTTPError(404)

    get.route = '/recover'