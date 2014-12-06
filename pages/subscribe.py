import datetime
import bottle
import json

import dbutils
import pages
from models import games, notificating, users
from modules import create_link, utils


def subscribe(user_id:int, game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if game.datetime.passed: raise bottle.HTTPError(404)
        if pages.auth.current().banned():
            return pages.PageBuilder("game", game=game, conflict=2)
        #if not pages.auth.current().activated():
        #    return pages.PageBuilder("game", game=game, conflict=3)
        if game.capacity() > 0 and len(game.subscribed()) == game.capacity():
            return pages.PageBuilder("game", game=game, conflict=4)
        if user_id in set(game.subscribed()):
            return pages.PageBuilder("game", game=game, conflict=5)
        another_game = games.user_game_intersection(user_id, game, dbconnection=db)
        if another_game:
            return pages.PageBuilder("game", game=game, conflict=1, conflict_data=another_game)
        games.subscribe(user_id, game_id, dbconnection=db)
        if game.datetime.tommorow or game.datetime.today:
            user = users.get(user_id, dbconnection=db) if user_id!=pages.auth.current().user_id() else pages.auth.current()
            message = 'На игру "{}" записался {}'.format(create_link.game(game), create_link.user(user))
            utils.spool_func(notificating.site.responsible, game.responsible_user_id(), message, 1, game_id,)
        game = games.get_by_id(game_id, dbconnection=db)
        return pages.PageBuilder("game", game=game)

def unsubscribe(user_id:int, game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if game.datetime.passed: raise bottle.HTTPError(404)
        if user_id not in set(game.subscribed()):
            return pages.PageBuilder("game", game=game, conflict=6)
        games.unsubscribe(user_id, game_id, dbconnection=db)
        if datetime.datetime.now()-game.datetime()<datetime.timedelta(days=3):
            user = users.get(user_id, dbconnection=db) if user_id!=pages.auth.current().user_id() else pages.auth.current()
            message = '{} отписался от игры "{}"'.format(create_link.user(user), create_link.game(game))
            utils.spool_func(notificating.site.responsible, game.responsible_user_id(), message, 1, game_id,)
        game = games.get_by_id(game_id, dbconnection=db)
        return pages.PageBuilder("game", game=game)

def reserve(user_id:int, game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if game.datetime.passed: raise bottle.HTTPError(404)
        #if not pages.auth.current().activated():
        #    return pages.PageBuilder("game", game=game, conflict=3)
        if pages.auth.current().banned():
            return pages.PageBuilder("game", game=game, conflict=2)
        if game.reserved()==0:
            return pages.PageBuilder("game", game=game, conflict=8)
        if len(game.subscribed())<game.capacity():
            return pages.PageBuilder("game", game=game, conflict=10)
        if user_id in set(game.reserved_people()):
            return pages.PageBuilder("game", game=game, conflict=7)
        if len(game.reserved_people())==game.reserved():
            return pages.PageBuilder("game", game=game, conflict=9)
        games.subscribe(user_id, game_id, True, dbconnection=db)
        game = games.get_by_id(game_id, dbconnection=db)
        return pages.PageBuilder("game", game=game)


def unreserve(user_id:int, game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if game.datetime.passed: raise bottle.HTTPError(404)
        if pages.auth.current().banned():
            return pages.PageBuilder("game", game=game, conflict=2)
        if user_id not in set(game.reserved_people()):
            return pages.PageBuilder("game", game=game, conflict=11)
        games.unsubscribe(user_id, game_id, dbconnection=db)
        game = games.get_by_id(game_id, dbconnection=db)
        return pages.PageBuilder("game", game=game)

def fromreserve(user_id:int, game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if user_id not in set(game.reserved_people()):
            return pages.PageBuilder("game", game=game, conflict=11)
        if user_id in set(game.subscribed()):
            return pages.PageBuilder("game", game=game, conflict=5)
        if game.capacity() > 0 and len(game.subscribed()) == game.capacity():
            return pages.PageBuilder("game", game=game, conflict=4)
        games.unsubscribe(user_id, game_id, dbconnection=db)
        games.subscribe(user_id, game_id, dbconnection=db)
        game = games.get_by_id(game_id, dbconnection=db)
        return pages.PageBuilder("game", game=game)


@pages.get('/games/subscribe/<game_id:int>')
@pages.only_ajax
@pages.only_loggedin
def get_subscibe(game_id:int):
    user_id = pages.auth.current().user_id()
    tab_name = bottle.request.query.get('tab_name')
    page = subscribe(user_id, game_id)
    page.add_param('tab_name', tab_name)
    return page

@pages.get('/games/subscribe/<game_id:int>/<user_id:int>')
@pages.only_organizers
def admin_subscribe(game_id:int, user_id:int):
    resp = subscribe(user_id, game_id)
    if 'conflict' in resp:
        if bottle.request.is_ajax:
            return json.dumps({'error_code':resp.param('conflict')})
        return pages.templates.message('Ошибка', 'Конфликт: {}'.format(resp.param('conflict')))
    if bottle.request.is_ajax:
        return json.dumps({'error_code':0})
    raise bottle.redirect(pages.referer('/games/{}'.format(game_id)))


@pages.get('/games/unsubscribe/<game_id:int>')
@pages.only_ajax
@pages.only_loggedin
def get_unsubscribe(game_id:int):
    user_id = pages.auth.current().user_id()
    tab_name = bottle.request.query.get('tab_name')
    page = unsubscribe(user_id, game_id)
    page.add_param('tab_name', tab_name)
    return page


@pages.get('/games/unsubscribe/<game_id:int>/<user_id:int>')
@pages.only_organizers
def admin_unsubscribe(game_id:int, user_id:int):
    resp = unsubscribe(user_id, game_id)
    if 'conflict' in resp:
        if bottle.request.is_ajax:
            return json.dumps({'error_code':resp.param('conflict')})
        return pages.templates.message('Ошибка', 'Конфликт: {}'.format(resp.param('conflict')))
    if bottle.request.is_ajax:
        return json.dumps({'error_code':0})
    raise bottle.redirect(pages.referer('/games/{}'.format(game_id)))


@pages.get('/games/reserve/<game_id:int>')
@pages.only_ajax
@pages.only_loggedin
def get_reserve(game_id:int):
    user_id = pages.auth.current().user_id()
    tab_name = bottle.request.query.get('tab_name')
    page = reserve(user_id, game_id)
    page.add_param('tab_name', tab_name)
    return page


@pages.get('/games/reserve/<game_id:int>/<user_id:int>')
@pages.only_organizers
def admin_reserve(game_id:int, user_id:int):
    resp = reserve(user_id, game_id)
    if 'conflict' in resp:
        if bottle.request.is_ajax:
            return json.dumps({'error_code':resp.param('conflict')})
        return pages.templates.message('Ошибка', 'Конфликт: {}'.format(resp.param('conflict')))
    if bottle.request.is_ajax:
        return json.dumps({'error_code':0})
    raise bottle.redirect(pages.referer('/games/{}'.format(game_id)))


@pages.get('/games/unreserve/<game_id:int>')
@pages.only_ajax
@pages.only_loggedin
def get_unreserve(game_id:int):
    user_id = pages.auth.current().user_id()
    tab_name = bottle.request.query.get('tab_name')
    page = unreserve(user_id, game_id)
    page.add_param('tab_name', tab_name)
    return page


@pages.get('/games/unreserve/<game_id:int>/<user_id:int>')
@pages.only_organizers
def admin_unreserve(game_id:int, user_id:int):
    resp = unreserve(user_id, game_id)
    if 'conflict' in resp:
        if bottle.request.is_ajax:
            return json.dumps({'error_code':resp.param('conflict')})
        return pages.templates.message('Ошибка', 'Конфликт: {}'.format(resp.param('conflict')))
    if bottle.request.is_ajax:
        return json.dumps({'error_code':0})
    raise bottle.redirect(pages.referer('/games/{}'.format(game_id)))


@pages.get('/games/fromreserve/<game_id:int>')
@pages.only_ajax
@pages.only_loggedin
def get_fromreserve(game_id:int):
    user_id = pages.auth.current().user_id()
    tab_name = bottle.request.query.get('tab_name')
    page = fromreserve(user_id, game_id)
    page.add_param('tab_name', tab_name)
    return page


@pages.get('/games/fromreserve/<game_id:int>/<user_id:int>')
@pages.only_organizers
def admin_fromreserve(game_id:int, user_id:int):
    resp = fromreserve(user_id, game_id)
    if 'conflict' in resp:
        if bottle.request.is_ajax:
            return json.dumps({'error_code':resp.param('conflict')})
        return pages.templates.message('Ошибка', 'Конфликт: {}'.format(resp.param('conflict')))
    if bottle.request.is_ajax:
        return json.dumps({'error_code':0})
    raise bottle.redirect(pages.referer('/games/{}'.format(game_id)))