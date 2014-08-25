import bottle

import pages


class Reloader(pages.Page):
    def get(self, page_name:str):
        if pages.loggedin() and pages.getadminlevel() == 1:
            pages.controller.reload(page_name)
            raise bottle.redirect('/')
        raise bottle.HTTPError(404)

    get.route = '/reload/<page_name>'