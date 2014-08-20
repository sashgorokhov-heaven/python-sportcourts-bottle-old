import bottle

import pages
import modules
import modules.dbutils


class Games(pages.Page):
    path = ['games']

    def execute(self, method:str):
        if method == 'GET':
            return self.get().template()

    @pages.setlogin
    @pages.handleerrors('games')
    def get(self):
        if 'game_id' in bottle.request.query:
            with modules.dbutils.dbopen() as db:
                modules.dbutils.get(db).game(bottle.request.query.get('game_id'))
                if len(db.last()) == 0:
                    raise bottle.HTTPError(404)
                game = db.last()[0]
                game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
                game['region'] = modules.dbutils.get(db).region(game['region_id'])[0]
                game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
                game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
                game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
                game.pop('city_id')
                game.pop('region_id')
                game.pop('court_id')
                modules.dbutils.strdates(game)
                subscribed = list(filter(lambda x: x != '', map(lambda x: x.strip(), game['subscribed'].split(','))))
                if pages.loggedin() and str(pages.getuserid()) in set(subscribed):
                    game['is_subscribed'] = True
                else:
                    game['is_subscribed'] = False
                if len(subscribed) > 0:
                    sql = "SELECT user_id, first_name, last_name FROM users WHERE user_id IN ({})".format(
                        ','.join(subscribed))
                    db.execute(sql, ['user_id', 'first_name', 'last_name'])
                    game['subscribed'] = {'count': len(db.last()), 'users': db.last()}
                else:
                    game['subscribed'] = {'count': 0, 'users': list()}
                return pages.Template('game', game=game, standalone=True)
        with modules.dbutils.dbopen() as db:
            sql = "SELECT *  FROM games WHERE city_id=1 AND datetime>NOW() ORDER BY datetime ASC LIMIT 20;"
            db.execute(sql, modules.dbutils.dbfields['games'])
            games = list()
            for game in db.last():
                game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
                game['region'] = modules.dbutils.get(db).region(game['region_id'])[0]
                game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
                game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
                game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
                game.pop('city_id')
                game.pop('region_id')
                game.pop('court_id')
                modules.dbutils.strdates(game)
                subscribed = list(filter(lambda x: x != '', map(lambda x: x.strip(), game['subscribed'].split(','))))
                if pages.loggedin() and str(pages.getuserid()) in set(subscribed):
                    game['is_subscribed'] = True
                else:
                    game['is_subscribed'] = False
                if len(subscribed) > 0:
                    sql = "SELECT user_id, first_name, last_name FROM users WHERE user_id IN ({})".format(
                        ','.join(subscribed))
                    db.execute(sql, ['user_id', 'first_name', 'last_name'])
                    game['subscribed'] = {'count': len(db.last()), 'users': db.last()}
                else:
                    game['subscribed'] = {'count': 0, 'users': list()}
                games.append(game)
            return pages.Template('games', games=games)