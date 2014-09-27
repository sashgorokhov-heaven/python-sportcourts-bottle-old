import bottle, pages, uwsgi


class Reloader(pages.Page):
    def get(self, page_name:str):
        if pages.auth_dispatcher.admin():
            if page_name == 'all':
                uwsgi.reload()
                raise bottle.redirect(bottle.request.get_header("Referer", "/"))
            pages.controller.reload(page_name)
            raise bottle.redirect(bottle.request.get_header("Referer", "/"))
        raise bottle.HTTPError(404)

    get.route = '/reload/<page_name>'