import pages
import bottle


class Og(pages.Page):
    def get(self, name):
        return bottle.static_file(name, '/bsp/data/images/og/')

    get.route = "/og/<name>"