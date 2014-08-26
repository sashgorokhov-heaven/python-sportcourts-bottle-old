import bottle

from modules.utils import beautifuldate, beautifultime, beautifulday
import pages
import modules
import modules.dbutils


class Games(pages.Page):
    def post_submit_add(self):
        with modules.dbutils.dbopen() as db:
            params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
            params.pop('submit_add')
            params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
            params.pop('date')
            params.pop('time')
            sql = """\
                SELECT game_id FROM games WHERE court_id={court_id} AND (\
                (DATETIME BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE) OR \
                (DATETIME + INTERVAL {duration} MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE));\
                """.format(
                court_id=params['court_id'],
                datetime=params['datetime'],
                duration=params['duration'].encode().split(b' ')[0].decode())
            db.execute(sql)
            if len(db.last()) > 0:
                return pages.PageBuilder('404', error='Обнаружен конфликт',
                                      error_description='В это время игра уже идет')
            sql = 'INSERT INTO games ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
            db.execute(sql)
            db.execute('SELECT last_insert_id() FROM games', ['game_id'])
            return bottle.redirect('/games?game_id={}'.format(db.last()[0]['game_id']))

    def post_submit_edit(self):
        with modules.dbutils.dbopen() as db:
            params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
            params.pop('submit_edit')
            params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
            params.pop('date')
            game_id = params['game_id']
            params.pop('game_id')
            params.pop('time')
            sql = 'UPDATE games SET {} WHERE game_id={}'.format(
                ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
                game_id)
            db.execute(sql)
            raise bottle.redirect('/games?game_id={}'.format(game_id))

    def post(self):
        if not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)
        if 'submit_add' in bottle.request.forms:
            return self.post_submit_add()
        if 'submit_edit' in bottle.request.forms:
            return self.post_submit_edit()
        raise bottle.HTTPError(404)

    def get_edit(self):
        if not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)
        with modules.dbutils.dbopen() as db:
            game_id = bottle.request.query.get('edit')
            modules.dbutils.get(db).game(game_id)
            if len(db.last()) == 0:
                raise bottle.HTTPError(404)
            game = db.last()[0]
            game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
            game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
            game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
            game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
            sports = db.execute("SELECT sport_id, title FROM sport_types")
            game_types = db.execute("SELECT type_id, sport_type, title FROM game_types")
            cities = db.execute("SELECT city_id, title FROM cities")
            courts = db.execute("SELECT court_id, city_id, title FROM courts")
            game.pop('city_id')
            game.pop('court_id')
            modules.dbutils.strdates(game)
            subscribed = list(filter(lambda x: x != '', map(lambda x: x.strip(), game['subscribed'].split(','))))
            if len(subscribed) > 0:
                sql = "SELECT user_id, first_name, last_name, phone FROM users WHERE user_id IN ({})".format(
                    ','.join(subscribed))
                db.execute(sql, ['user_id', 'first_name', 'last_name', 'phone'])
                game['subscribed'] = {'count': len(db.last()), 'users': db.last()}
            else:
                game['subscribed'] = {'count': 0, 'users': list()}
            return pages.PageBuilder('editgame', game=game, sports=sports,
                                  game_types=game_types, cities=cities, courts=courts)

    def get_add(self):
        if not pages.auth_dispatcher.organizer():
            return bottle.HTTPError(404)
        with modules.dbutils.dbopen() as db:
            sports = db.execute("SELECT sport_id, title FROM sport_types")
            game_types = db.execute("SELECT type_id, sport_type, title FROM game_types")
            cities = db.execute("SELECT city_id, title FROM cities")
            courts = db.execute("SELECT court_id, city_id, title FROM courts")
            return pages.PageBuilder("addgame", sports=sports,
                                  game_types=game_types, cities=cities, courts=courts)

    def get_game_id(self):
        with modules.dbutils.dbopen() as db:
            modules.dbutils.get(db).game(bottle.request.query.get('game_id'))
            if len(db.last()) == 0:
                return bottle.HTTPError(404)
            game = db.last()[0]
            game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
            game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
            game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
            game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
            game.pop('city_id')
            game.pop('court_id')
            modules.dbutils.strdates(game)
            game['datetime'] = (
                beautifuldate(game['datetime']), beautifultime(game['datetime']), beautifulday(game['datetime']))
            subscribed = list(filter(lambda x: x != '', map(lambda x: x.strip(), game['subscribed'].split(','))))
            if pages.auth_dispatcher.loggedin() and str(pages.auth_dispatcher.getuserid()) in set(subscribed):
                game['is_subscribed'] = True
            else:
                game['is_subscribed'] = False
            if len(subscribed) > 0:
                sql = "SELECT user_id, first_name, last_name, phone FROM users WHERE user_id IN ({})".format(
                    ','.join(subscribed))
                db.execute(sql, ['user_id', 'first_name', 'last_name', 'phone'])
                game['subscribed'] = {'count': len(db.last()), 'users': db.last()}
            else:
                game['subscribed'] = {'count': 0, 'users': list()}
            return pages.PageBuilder('game', game=game, standalone=True)

    def get(self):
        if 'edit' in bottle.request.query:
            return self.get_edit()
        if 'delete' in bottle.request.query:
            if not pages.auth_dispatcher.organizer():
                return bottle.HTTPError(404)
            with modules.dbutils.dbopen() as db:
                db.execute("DELETE FROM games WHERE game_id={}".format(bottle.request.query.get('delete')))
                return bottle.redirect('/games')
        if 'add' in bottle.request.query:
            return self.get_add()
        if 'game_id' in bottle.request.query:
            return self.get_game_id()
        with modules.dbutils.dbopen() as db:
            sql = "SELECT *  FROM games WHERE city_id=1 AND datetime>NOW() ORDER BY datetime ASC LIMIT 20;"
            allgames = db.execute(sql, modules.dbutils.dbfields['games'])
            sports = db.execute("SELECT * FROM sport_types", modules.dbutils.dbfields['sport_types'])
            games = list()
            for game in allgames:
                game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
                game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
                game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
                game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
                game.pop('city_id')
                game.pop('court_id')
                modules.dbutils.strdates(game)
                game['datetime'] = (
                    beautifuldate(game['datetime']), beautifultime(game['datetime']), beautifulday(game['datetime']))
                subscribed = list(filter(lambda x: x != '', map(lambda x: x.strip(), game['subscribed'].split(','))))
                if pages.auth_dispatcher.loggedin() and str(pages.auth_dispatcher.getuserid()) in set(subscribed):
                    game['is_subscribed'] = True
                else:
                    game['is_subscribed'] = False
                if len(subscribed) > 0:
                    sql = "SELECT user_id, first_name, last_name, phone FROM users WHERE user_id IN ({})".format(
                        ','.join(subscribed))
                    db.execute(sql, ['user_id', 'first_name', 'last_name', 'phone'])
                    game['subscribed'] = {'count': len(db.last()), 'users': db.last()}
                else:
                    game['subscribed'] = {'count': 0, 'users': list()}
                games.append(game)
            return pages.PageBuilder('games', games=games, sports=sports)

    get.route = '/games'
    post.route = get.route