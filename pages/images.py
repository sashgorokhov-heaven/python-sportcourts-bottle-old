import os
import bottle

import pages


class Images(pages.Page):
    def get_court_image(self, name):
        return bottle.static_file("{}.jpg".format(name), '/bsp/data/images/courts/')

    def get_static_image(self, name):
        return bottle.static_file(name, '/bsp/data/images/static/')

    def get_avatar_image(self, name):
        filename = str(name)
        fullaname = '/bsp/data/avatars/{}.jpg'.format(filename)
        if not os.path.exists(fullaname):
            filename = 'blank'
        return bottle.static_file('{}.jpg'.format(filename), '/bsp/data/avatars/')

    def get_og_image(self, name):
        return bottle.static_file(name, '/bsp/data/images/og/')

    def get(self, what, name):
        if what == 'courts':
            return self.get_court_image(name)
        if what == 'static':
            return self.get_static_image(name)
        if what == 'avatars':
            return self.get_avatar_image(name)
        if what == 'og':
            return self.get_og_image(name)
        raise bottle.HTTPError(404)


    get.route = '/images/<what>/<name>'
