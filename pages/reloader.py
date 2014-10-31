import os
import bottle
import config

import pages
from modules.myuwsgi import uwsgi, uwsgidecorators


class Reloader(pages.Page):
    def get(self, page_name:str):
        if pages.auth.current().userlevel.admin():
            if page_name == 'all':
                uwsgi.reload()
                raise bottle.redirect(bottle.request.get_header("Referer", "/"))
            pages.controller.reload(page_name)
            raise bottle.redirect(bottle.request.get_header("Referer", "/"))
        raise bottle.HTTPError(404)

    @uwsgidecorators.filemon(os.path.join(config.paths.server.root, 'pages'))
    def reload_on_pages_change(self, *args):
        uwsgi.reload()

    get.route = '/reload/<page_name>'