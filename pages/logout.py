import bottle

import pages


class Logout(pages.Page):
    def get(self):
        if pages.loggedin():
            bottle.response.delete_cookie('user_id')
        raise bottle.redirect('/')

    get.route = '/logout'