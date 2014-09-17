import bottle

import pages


class Reloader(pages.Page):
    def get(self, page_name:str):
        if pages.auth_dispatcher.admin():
            pages.controller.reload(page_name)
            raise bottle.redirect('/')
        raise bottle.HTTPError(404)

    get.route = '/reload/<page_name>'