import bottle
import os
import pages
import modules.logging


class Logs(pages.Page):
    def get_last_error(self):
        if not os.path.exists(modules.logging._TRACEBACK_FILE):
            raise bottle.HTTPError(404)
        error = open(modules.logging._TRACEBACK_FILE, 'r').read()
        return pages.templates.message("Последняя ошибка: ", error.replace("\n", "<br>"))

    def get_logs(self):
        if not os.path.exists(modules.logging._LOG_FILE):
            raise bottle.HTTPError(404)
        logs = open(modules.logging._LOG_FILE, 'r').read()
        return pages.templates.message("Логи: ", logs.replace("\n", "<br>"))

    def get(self, **kwargs):
        if not pages.auth_dispatcher.admin():
            raise bottle.HTTPError(404)
        if 'lasterror' in bottle.request.query:
            return self.get_last_error()
        return self.get_logs()

    get.route = '/logs'
