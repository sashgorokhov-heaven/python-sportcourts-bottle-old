import os

import bottle

import config
import pages


class Static(pages.Page):
    def get(self, path:str):
        return bottle.static_file(path, os.path.join(config.server_root, 'static/view'))

    get.route = '/view/<path:path>'