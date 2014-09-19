import bottle
import os
import pages
from modules import logging


class LastError(pages.Page):
    def get(self, **kwargs):
        if not pages.auth_dispatcher.admin() or not os.path.exists(logging._TRACEBACK_FILE):
            raise bottle.HTTPError(404)
        error = open(logging._TRACEBACK_FILE, 'r').read()
        return pages.templates.message("Последняя ошибка: ", error.replace("\n", "<br>"))

    get.route = '/lasterror'
