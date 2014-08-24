import os

import bottle

import modules
import pages


class Static(pages.Page):
    def get(self, path:str):
        return bottle.static_file(path, os.path.join(modules.config['server_root'], 'static/view'))

    get.route = '/view/<path:path>'