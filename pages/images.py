import bottle

import pages


class Images(pages.Page):
    def get(self, court_id:int):
        return bottle.static_file("{}.jpg".format(court_id), '/bsp/data/images/courts/')

    get.route = '/images/courts/<court_id:int>'
