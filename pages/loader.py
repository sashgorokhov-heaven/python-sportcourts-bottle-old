import bottle

import pages


class Loader(pages.Page):
    def get(self):
        if pages.auth.current().userlevel.admin():
            pages.controller.loadpages()
            raise bottle.redirect('/')
        raise bottle.HTTPError(404)

    get.route = '/loadpages'
