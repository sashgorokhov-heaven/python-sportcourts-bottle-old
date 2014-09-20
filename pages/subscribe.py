import bottle
from modules.utils import beautifuldate, beautifultime, beautifulday

import pages
from models import games, notifications, sport_types
from modules import dbutils, create_link


class Subscribe(pages.Page):
    def subscribe(self, game_id:int, user_id:int, unsubscribe:bool=True):
        try:
            if unsubscribe:
                games.unsubscribe(user_id, game_id)
            else:
                games.subscribe(user_id, game_id)
        except ValueError:
            pass

    def post(self):
        """
        game_id
        [unsubscribe]
        """
        if not pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.forms.get('game_id'))
        user_id = pages.auth_dispatcher.getuserid()
        unsubscribe = 'unsubscribe' in bottle.request.forms

        self.subscribe(game_id, user_id, unsubscribe)

        if not bottle.request.is_ajax:
            return ''

        tab_name = bottle.request.forms.get("tab_name")
        # sport_type = int(bottle.request.forms.get("tab_name"))

        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, detalized=True, dbconnection=db)
            if pages.auth_dispatcher.getuserid() in {user['user_id'] for user in game['subscribed']['users']}:
                game['is_subscribed'] = True
            else:
                game['is_subscribed'] = False
            game['parsed_datetime'] = (beautifuldate(game['datetime'], True),
                                       beautifultime(game['datetime']),
                                       beautifulday(game['datetime']))
            return pages.PageBuilder("game", tab_name=tab_name, game=game)


    def get(self):  # для ручного отписывания
        """
        game_id
        user_id
        [unsubscribe]
        """
        if not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.query.get('game_id'))
        user_id = int(bottle.request.query.get('user_id'))
        unsubscribe = 'unsubscribe' in bottle.request.query

        self.subscribe(game_id, user_id, unsubscribe)

        notifications.add(user_id,
                          'Вы были удалены с игры "{}"'.format(
                              games.get_by_id(game_id, fields=['game_id', 'description'])), 1)

        raise bottle.redirect('/games?edit={}'.format(game_id))

    post.route = '/subscribe'
    get.route = post.route