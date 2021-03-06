import bottle
import config
import modules
import pages
import modules.myuwsgi
import modules.backuper
import modules.timer


list(map(bottle.TEMPLATE_PATH.append, config.paths.server.views))
bottle.debug(config.debug)


@bottle.error(404)
def error404(error):
    return pages.PageBuilder('404').template()


application = bottle.default_app()

bottle.install(modules.exec_time_measure)

if config.standalone:
    bottle.run(host=config.server.ip, port=config.server.port, debug=config.debug)