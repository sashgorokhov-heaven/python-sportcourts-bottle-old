import bottle
import config
import pages


@pages.get(['/', '/main', '/index'])
def index():
    return pages.PageBuilder('index')


@pages.get('/about')
def about():
    return pages.PageBuilder('about')


@pages.get('/2015')
def promo():
    return pages.PageBuilder('2015')


@pages.get('/contacts')
def get():
    return pages.PageBuilder('contacts')


@bottle.get('/sitemap.xml')
def sitemap():
    return bottle.static_file('sitemap.xml', config.paths.server.static)


@bottle.get('/robots.txt')
def robots():
    return bottle.static_file('robots.txt', config.paths.server.static)