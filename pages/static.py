import bottle

import config
import pages


@pages.get('/view/<path:path>')
def static(path:str):
    return bottle.static_file(path, config.paths.server.static)