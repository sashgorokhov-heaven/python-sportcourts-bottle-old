import bottle

import config
import modules
import modules.myuwsgi


list(map(bottle.TEMPLATE_PATH.append, config.paths.server.views))
bottle.debug(config.debug)

import pages
import modules.backuper


@bottle.error(404)
def error404(error):
    return pages.PageBuilder('404').template()


application = bottle.default_app()

bottle.install(modules.exec_time_measure)