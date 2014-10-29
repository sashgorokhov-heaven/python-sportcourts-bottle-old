import bottle

import dbutils
import pages
from models import games, notifications
from modules import create_link


class Subscribe(pages.Page):
    def subscribe(self, user_id:int, game_id:int):
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, dbconnection=db)

            if game.datetime.passed: raise bottle.HTTPError(404)

            if pages.auth.current().banned():
                return pages.PageBuilder("game", game=game, conflict=2)

            if not pages.auth.current().activated():
                return pages.PageBuilder("game", game=game, conflict=3)

            if game.capacity() > 0 and len(game.subscribed()) == game.capacity():
                return pages.PageBuilder("game", game=game, conflict=4)

            if user_id in set(game.subscribed()):
                return pages.PageBuilder("game", game=game, conflict=5)

            another_game = games.user_game_intersection(user_id, game, dbconnection=db)
            if another_game:
                return pages.PageBuilder("game", game=game, conflict=1, conflict_data=another_game)

            games.subscribe(user_id, game_id, dbconnection=db)

            if game.datetime.tommorow or game.datetime.today:
                message = 'На игру "{}" записался {}'.format(create_link.game(game),
                                                             create_link.user(pages.auth.current()))
                notifications.add(game.responsible_user_id(), message, 1, game_id, 2)

            game = games.get_by_id(game_id, dbconnection=db)
            return pages.PageBuilder("game", game=game)

    def unsubscribe(self, user_id:int, game_id:int):
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, dbconnection=db)

            if game.datetime.passed: raise bottle.HTTPError(404)

            if user_id not in set(game.subscribed()):
                return pages.PageBuilder("game", game=game, conflict=6)

            games.unsubscribe(user_id, game_id, dbconnection=db)

            if game.datetime.tommorow or game.datetime.today:
                message = '{} отписался от игры "{}"'.format(create_link.user(pages.auth.current()),
                                                             create_link.game(game))
                notifications.add(game.responsible_user_id(), message, 1, game_id, 2)

            game = games.get_by_id(game_id, dbconnection=db)
            return pages.PageBuilder("game", game=game)

    def reserve(self, user_id:int, game_id:int):
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, dbconnection=db)

            if game.datetime.passed: raise bottle.HTTPError(404)

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


    def unreserve(self, user_id:int, game_id:int):
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, dbconnection=db)

            if game.datetime.passed: raise bottle.HTTPError(404)

            if user_id not in set(game.reserved_people()):
                return pages.PageBuilder("game", game=game, conflict=11)

            games.unsubscribe(user_id, game_id, dbconnection=db)

            game = games.get_by_id(game_id, dbconnection=db)
            return pages.PageBuilder("game", game=game)

    def fromreserve(self, user_id:int, game_id:int):
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

    def post(self):
        """
        game_id
        [unsubscribe]
        """
        if not pages.auth.loggedin():
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.forms.get('game_id'))
        user_id = pages.auth.current().user_id()
        action = bottle.request.forms.get('action')

        if not bottle.request.is_ajax:
            raise ValueError("Not ajax request")

        if action=='get' or action=='post' or action=='execute' or not hasattr(self, action):
            raise bottle.HTTPError(404)

        resp = getattr(self, action, None)(user_id, game_id)
        if not resp: raise bottle.HTTPError(404)

        resp.add_param('tab_name', bottle.request.forms.get("tab_name"))
        return resp

    def get(self):  # для ручного отписывания
        """
        game_id
        user_id
        [unsubscribe]
        """
        game_id = int(bottle.request.query.get('game_id'))
        user_id = int(bottle.request.query.get('user_id'))
        unsubscribe = 'unsubscribe' in bottle.request.query
        reserve = 'reserve' in bottle.request.query

        game = games.get_by_id(game_id)

        if game.responsible_user_id() != user_id and not pages.auth.current().userlevel.admin() and not pages.auth.current().userlevel.organizer():
            raise bottle.HTTPError(404)

        games.subscribe(user_id, game_id, reserved=reserve) if not unsubscribe else games.unsubscribe(user_id, game_id)

        if unsubscribe:
            notifications.add(user_id, 'Вы были удалены с игры "{}"'.format(create_link.game(game)), 1, game_id, 1)

        raise bottle.redirect('/games?edit={}'.format(game_id))

    post.route = '/subscribe'
    get.route = post.route