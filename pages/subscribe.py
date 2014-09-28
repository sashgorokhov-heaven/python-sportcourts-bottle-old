import bottle
from modules.utils import beautifuldate, beautifultime, beautifulday

import pages
from models import games, notifications, users
from modules import dbutils, create_link
import datetime, itertools


class Subscribe(pages.Page):
    def check_intersection(self, user_id:int, game:dict, db:dbutils.DBConnection) -> dict:
        query = """\
          SELECT game_id, description FROM games WHERE LOCATE('|{user_id}|', subscribed) AND (\
          (DATETIME BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE) OR \
          (DATETIME + INTERVAL {duration} MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE));\
          """.format(user_id=user_id, datetime=game['datetime'], duration=game['duration'])
        db.execute(query, ['game_id', 'description'])
        if len(db.last()) != 0:
            return db.last()[0]
        return dict()

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

        if not bottle.request.is_ajax:
            self.subscribe(game_id, user_id, unsubscribe)
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
            pdatetime = datetime.datetime(*itertools.chain(map(int, game['datetime'].split(' ')[0].split('-')),
                                                           map(int, game['datetime'].split(' ')[1].split(':'))))
            another_game = self.check_intersection(user_id, game, db)
            if len(another_game) > 0 and not unsubscribe:
                message = 'В это время вы уже записаны на игру "{}"'.format(create_link.game(another_game))
                return pages.PageBuilder("game", tab_name=tab_name, game=game, message=message)

            if pdatetime - datetime.timedelta(
                    days=1) <= datetime.datetime.now() <= pdatetime:
                user = users.get(user_id, fields=['user_id', 'first_name', 'last_name'], dbconnection=db)
                if not unsubscribe:
                    message = 'На игру "{}" записался {}'.format(create_link.game(game),
                                                                            create_link.user(user))
                else:
                    message = '{} отписался от игры "{}"'.format(create_link.user(user),
                                                                            create_link.game(game))
                notifications.add(game['responsible_user']['user_id'], message, 1, game_id, 2, dbconnection=db)
            self.subscribe(game_id, user_id, unsubscribe)
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
        game_id = int(bottle.request.query.get('game_id'))
        user_id = int(bottle.request.query.get('user_id'))
        unsubscribe = 'unsubscribe' in bottle.request.query

        if games.get_by_id(game_id, fields=['responsible_user_id'])[
            'responsible_user_id'] != user_id and not pages.auth_dispatcher.admin() and not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)

        self.subscribe(game_id, user_id, unsubscribe)

        notifications.add(user_id,
                          'Вы были удалены с игры "{}"'.format(
                              create_link.game(games.get_by_id(game_id, fields=['game_id', 'description']))), 1,
                          game_id, 1)

        raise bottle.redirect('/games?edit={}'.format(game_id))

    post.route = '/subscribe'
    get.route = post.route