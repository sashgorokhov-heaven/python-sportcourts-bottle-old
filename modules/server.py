import bottle

import modules
import modules.dbutils
import pages


bottle.TEMPLATE_PATH.append('views')
bottle.debug(modules.config['debug'])


@bottle.error(404)
def error404(error):
    return bottle.template('404')


@bottle.route('/', method=['POST', 'GET'])
@bottle.route('/<path:path>', method=['POST', 'GET'])
def route(path:str='', ):
    return pages.controller.execute(bottle.request.method, path)


application = bottle.default_app()

