import bottle, pages, uwsgi
import uwsgidecorators

class Reloader(pages.Page):
    def get(self, page_name:str):
        if pages.auth_dispatcher.admin():
            if page_name == 'all':
                uwsgi.reload()
                raise bottle.redirect(bottle.request.get_header("Referer", "/"))
            pages.controller.reload(page_name)
            raise bottle.redirect(bottle.request.get_header("Referer", "/"))
        raise bottle.HTTPError(404)

    @uwsgidecorators.filemon("/bsp/server/pages")
    @uwsgidecorators.filemon("/bsp/server/models")
    @uwsgidecorators.filemon("/bsp/server/modules")
    def reload_on_pages_change(self, *args):
        uwsgi.reload()

    get.route = '/reload/<page_name>'