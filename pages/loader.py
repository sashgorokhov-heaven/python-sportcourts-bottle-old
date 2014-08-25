import bottle

import pages


class Loader(pages.Page):
    def get(self):
        if pages.loggedin() and pages.getadminlevel() == 1:
            pages.controller.loadpages()
            raise bottle.redirect('/')
        raise bottle.HTTPError(404)

    get.route = '/loadpages'
