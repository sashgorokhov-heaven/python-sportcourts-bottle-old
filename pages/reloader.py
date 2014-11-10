import os
import bottle
import config

import pages
from modules.myuwsgi import uwsgi, uwsgidecorators


class Reloader(pages.Page):
    def get(self):
        if pages.auth.current().userlevel.admin():
            referer = bottle.request.get_header("Referer", "/")
            page_name = bottle.request.query.get('page_name', 'all')
            if page_name == 'all':
                uwsgi.reload()
            else:
                pages.controller.reload(page_name)
            raise bottle.redirect(referer)
        raise bottle.HTTPError(404)

    @uwsgidecorators.filemon(os.path.join(config.paths.server.root, 'pages'))
    def reload_on_pages_change(self, *args):
        uwsgi.reload()

    get.route = '/admin/reload'