import os
import bottle
import hashlib

import pages
from models import games


_hashes = dict() # filename -> hash


def _hash(filename:str) -> bytes:
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            b = f.read(1024)
            if not b:
                break
            hasher.update(b)
    return hasher.hexdigest()

def _can_cache(filename:str):
    current_hash = _hash(filename)
    if filename in _hashes:
        if current_hash == _hashes[filename]:
            return True
        else:
            _hashes[filename] = current_hash
            return False
    else:
        _hashes[filename] = current_hash
        return True

def cache(func):
    def wrapper(*args, **kwargs):
        resp, filename = func(*args, **kwargs)
        #print('Cache', filename, '? ', end='')
        #if not _can_cache(filename):
            #print('Nope')
        resp.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        resp.set_header('Pragma', 'no-cache')
        resp.set_header('Expires', 0)
        #else:
        #    print('Yep')
        return resp
    return wrapper


class Images(pages.Page):
    def get_court_image(self, name):
        return bottle.static_file("{}.jpg".format(name), '/bsp/data/images/courts/')

    def get_static_image(self, name):
        return bottle.static_file(name, '/bsp/data/images/static/')

    @cache
    def get_avatar_image(self, name):
        filename = str(name)
        dirname = '/bsp/data/images/avatars'
        fullaname = os.path.join(dirname, filename+'.jpg')
        if not os.path.exists(fullaname):
            filename = 'blank'
            return bottle.static_file('{}.jpg'.format(filename), dirname), os.path.join(dirname, '{}.jpg'.format(filename))
        if 'sq' in bottle.request.query:
            filename = filename+'_sq'
        return bottle.static_file('{}.jpg'.format(filename), dirname), os.path.join(dirname, '{}.jpg'.format(filename))

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
