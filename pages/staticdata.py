import bottle
import pages


class StaticData(pages.Page):
    def get(self, name):
        return bottle.static_file(name, '/bsp/data/images/static/')

    get.route = "/images/static/<name>"