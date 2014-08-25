import bottle

import pages


class Logout(pages.Page):
    def get(self):
        pages.auth_dispatcher.logout()
        raise bottle.redirect('/')

    get.route = '/logout'