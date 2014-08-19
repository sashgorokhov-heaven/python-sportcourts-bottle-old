import os

import bottle

import modules
import pages


bottle.TEMPLATE_PATH.append('views')
bottle.debug(modules.config['debug'])


@bottle.error(404)
def error404(error):
    return pages.Template('404', login=True).template()


@bottle.get('/avatars/<user_id:int>')
def route_avatars(user_id:int):
    filename = str(user_id)
    fullaname = '/apiserver/data/avatars/{}.jpg'.format(filename)
    if not os.path.exists(fullaname):
        filename = 'blank'
    return bottle.static_file('{}.jpg'.format(filename), '/apiserver/data/avatars/')

@bottle.route('/', method=['POST', 'GET'])
@bottle.route('/<path:path>', method=['POST', 'GET'])
def route(path:str='', ):
    return pages.controller.execute(bottle.request.method, path)


application = bottle.default_app()

