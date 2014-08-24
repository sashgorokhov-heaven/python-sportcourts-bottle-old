import os

import bottle

import modules
import pages


bottle.TEMPLATE_PATH.append('views')
bottle.debug(modules.config['debug'])


@bottle.error(404)
def error404(error):
    return pages.Template('404', login=True).template()


@bottle.get('/avatars/<user_id>')
def route_avatars(user_id:str):
    filename = str(user_id)
    fullaname = '/bsp/data/avatars/{}.jpg'.format(filename)
    if not os.path.exists(fullaname):
        filename = 'blank'
    return bottle.static_file('{}.jpg'.format(filename), '/bsp/data/avatars/')


@bottle.get('/images/courts/<court_id:int>')
def route_images(court_id:str):
    print(court_id)
    return bottle.static_file("{}.jpg".format(court_id), '/bsp/data/images/courts/')


@bottle.route('/', method=['POST', 'GET'])
@bottle.route('/<path:path>', method=['POST', 'GET'])
def route(path:str='', ):
    return pages.controller.execute(bottle.request.method, path)


application = bottle.default_app()

