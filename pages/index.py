import bottle
import config
import pages
import dbutils

from models import users


@pages.get(['/', '/main', '/index'])
def index():
    return pages.PageBuilder('index')


@pages.get('/about')
def about():
    return pages.PageBuilder('about')


@pages.get('/2015')
def promo():
    return pages.PageBuilder('2015')


@pages.get('/referal/<user_id:int>')
def referal(user_id:int):
    with dbutils.dbopen() as db:
        user = users.get(user_id, dbconnection=db)
        if len(user) == 0:
            raise bottle.HTTPError(404)
        return pages.PageBuilder('referal', user=user)


@pages.get('/contacts')
def get():
    return pages.PageBuilder('contacts')


@bottle.get('/sitemap.xml')
def sitemap():
    return bottle.static_file('sitemap.xml', config.paths.server.static)


@bottle.get('/robots.txt')
def robots():
    return bottle.static_file('robots.txt', config.paths.server.static)