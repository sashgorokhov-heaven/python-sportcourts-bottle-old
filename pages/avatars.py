import os

import bottle

import pages


class Avatars(pages.Page):
    def get(self, user_id:int):
        filename = str(user_id)
        fullaname = '/bsp/data/avatars/{}.jpg'.format(filename)
        if not os.path.exists(fullaname):
            filename = 'blank'
        return bottle.static_file('{}.jpg'.format(filename), '/bsp/data/avatars/')

    get.route = '/avatars/<user_id:int>'