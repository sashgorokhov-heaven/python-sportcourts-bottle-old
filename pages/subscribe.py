import bottle

import dbutils
import pages
from models import games, notifications
from modules import create_link


class Subscribe(pages.Page):
    def subscribe(self, game_id:int, user_id:int, unsubscribe:bool, db):
        try:
            if unsubscribe:
                games.unsubscribe(user_id, game_id, dbconnection=db)
            else:
                games.subscribe(user_id, game_id, dbconnection=db)
        except ValueError:
            pass

    def post(self):
        """
        game_id
        [unsubscribe]
        """
        if not pages.auth.loggedin():
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.forms.get('game_id'))
        user_id = pages.auth.current().user_id()
        unsubscribe = 'unsubscribe' in bottle.request.forms

        if not bottle.request.is_ajax:
            raise ValueError("Not ajax request")

        tab_name = bottle.request.forms.get("tab_name")
        # sport_type = int(bottle.request.forms.get("tab_name"))

        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, dbconnection=db)

            if not unsubscribe:
                if pages.auth.current().banned():
                    return pages.PageBuilder("game", tab_name=tab_name, game=game, conflict=2)

                if not pages.auth.current().activated():
                    return pages.PageBuilder("game", tab_name=tab_name, game=game, conflict=3)

                another_game = games.user_game_intersection(user_id, game, dbconnection=db)
                if another_game:
                    return pages.PageBuilder("game", tab_name=tab_name, game=game, conflict=1, conflict_data=another_game)

            self.subscribe(game_id, user_id, unsubscribe, db)

            if game.datetime.tommorow or game.datetime.today:
                if not unsubscribe:
                    message = 'На игру "{}" записался {}'.format(create_link.game(game),
                                                                            create_link.user(pages.auth.current()))
                else:
                    message = '{} отписался от игры "{}"'.format(create_link.user(pages.auth.current()),
                                                                            create_link.game(game))
                notifications.add(game.responsible_user_id(), message, 1, game_id, 2)
            game = games.get_by_id(game_id, dbconnection=db)
            return pages.PageBuilder("game", tab_name=tab_name, game=game)


    def get(self):  # для ручного отписывания
        """
        game_id
        user_id
        [unsubscribe]
        """
        game_id = int(bottle.request.query.get('game_id'))
        user_id = int(bottle.request.query.get('user_id'))
        unsubscribe = 'unsubscribe' in bottle.request.query

        game = games.get_by_id(game_id)

        if game.responsible_user_id() != user_id and not pages.auth.current().userlevel.admin() and not pages.auth.current().userlevel.organizer():
            raise bottle.HTTPError(404)

        self.subscribe(game_id, user_id, unsubscribe, None)

        notifications.add(user_id, 'Вы были удалены с игры "{}"'.format(create_link.game(game)), 1, game_id, 1)

        raise bottle.redirect('/games?edit={}'.format(game_id))

    post.route = '/subscribe'
    get.route = post.route