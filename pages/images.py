import os
import bottle

import pages
from models import games


def no_cache(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        resp.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        resp.set_header('Pragma', 'no-cache')
        resp.set_header('Expires', 0)
        return resp
    return wrapper


class Images(pages.Page):
    def get_court_image(self, name):
        return bottle.static_file("{}.jpg".format(name), '/bsp/data/images/courts/')

    def get_static_image(self, name):
        return bottle.static_file(name, '/bsp/data/images/static/')

    @no_cache
    def get_avatar_image(self, name):
        filename = str(name)
        dirname = '/bsp/data/images/avatars'
        fullaname = os.path.join(dirname, filename+'.jpg')
        if not os.path.exists(fullaname):
            filename = 'blank'
            return bottle.static_file('{}.jpg'.format(filename), '/bsp/data/images/avatars/')
        if 'sq' in bottle.request.query:
            filename = filename+'_sq'
        return bottle.static_file('{}.jpg'.format(filename), '/bsp/data/images/avatars/')

    def get_og_image(self, name):
        return bottle.static_file(name, '/bsp/data/images/og/')

    def get_report_image(self, game_id):
        game = games.get_by_id(game_id, fields=['created_by', 'responsible_user_id'])
        if pages.auth_dispatcher.getuserid() == game['responsible_user_id'] or pages.auth_dispatcher.getuserid() == \
                game['created_by'] or pages.auth_dispatcher.admin():
            return bottle.static_file(game_id + '.jpg', '/bsp/data/images/reports/')
        raise bottle.HTTPError(404)

    def get(self, what, name):
        if what == 'courts':
            return self.get_court_image(name)
        if what == 'static':
            return self.get_static_image(name)
        if what == 'avatars':
            return self.get_avatar_image(name)
        if what == 'og':
            return self.get_og_image(name)
        if what == 'reports':
            return self.get_report_image(name)
        raise bottle.HTTPError(404)


    get.route = '/images/<what>/<name>'
