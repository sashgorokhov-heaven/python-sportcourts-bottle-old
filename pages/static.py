import bottle

import config
import pages


class Static(pages.Page):
    def get(self, path:str):
        return bottle.static_file(path, config.paths.server.static)

    get.route = '/view/<path:path>'