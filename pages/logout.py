import bottle

import pages


class Logout(pages.Page):
    def get(self):
        pages.auth_dispatcher.logout()
        raise bottle.redirect(bottle.request.get_header("Referer", "/"))

    get.route = '/logout'