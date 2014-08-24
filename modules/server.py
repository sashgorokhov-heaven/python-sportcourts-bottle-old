import bottle

import modules


bottle.TEMPLATE_PATH.append('views')
bottle.debug(modules.config['debug'])

import pages


@bottle.error(404)
def error404(error):
    return pages.Template('404', login=True).template()


application = bottle.default_app()

bottle.install(modules.exec_time_measure)

