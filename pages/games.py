import datetime

import bottle

import pages
import modules
import modules.dbutils


months = ['Января', 'Февраля',
          'Марта', 'Апреля',
          'Мая', 'Июня', 'Июля',
          'Августа', 'Сентября',
          'Октября', 'Ноября', 'Декабря']
days = ['Понедельник', 'Вторник', 'Среда',
        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def beautifuldate(datetime:str):
    date, day = datetime.split(' ')[0].split('-')[1:]
    return '{} {}'.format(day, months[int(date) - 1])


def beautifultime(datetime:str):
    return datetime.split(' ')[-1]


def beautifulday(datetime_:str):
    return days[datetime.date(*list(map(int, datetime_.split(' ')[0].split('-')))).weekday()]


class Games(pages.Page):
    path = ['games']

    def execute(self, method:str):
        if method == 'POST':
            data = self.post()
            if isinstance(data, pages.Template):
                return data.template()
            return data
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    def post(self):
        if not pages.loggedin():
            raise bottle.HTTPError(404)
        if 'submit_add' in bottle.request.forms:
            with modules.dbutils.dbopen() as db:
                params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
                params.pop('submit_add')
                params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
                params.pop('date')
                params.pop('time')
                sql = 'INSERT INTO games ({dbkeylist}) VALUES ({dbvaluelist})'
                keylist = list(params.keys())
                sql = sql.format(
                    dbkeylist=', '.join(keylist),
                    dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
                db.execute(sql)
                db.execute('SELECT last_insert_id() FROM games', ['game_id'])
                raise bottle.redirect('/games?game_id={}'.format(db.last()[0]['game_id']))
        elif 'submit_edit' in bottle.request.forms:
            pass
        else:
            raise bottle.HTTPError(404)

    @pages.setlogin
    @pages.handleerrors('games')
    def get(self):
        if 'edit' in bottle.request.query:
            if not pages.loggedin():
                raise bottle.HTTPError(404)
            with modules.dbutils.dbopen() as db:
                game_id = bottle.request.query.get('edit')
                modules.dbutils.get(db).game(game_id)
                if len(db.last()) == 0:
                    raise bottle.HTTPError(404)
                game = db.last()[0]
                game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
                # game['region'] = modules.dbutils.get(db).region(game['region_id'])[0]
                game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
                game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
                game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
                sports = db.execute("SELECT sport_id, title FROM sport_types")
                game_types = db.execute("SELECT type_id, title FROM game_types")
                cities = db.execute("SELECT city_id, title FROM cities")
                courts = db.execute("SELECT court_id, title FROM courts")
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
                return pages.Template('editgame', game=game, sports=sports,
                                      game_types=game_types, cities=cities, courts=courts)
        if 'delete' in bottle.request.query:
            if not pages.loggedin():
                raise bottle.HTTPError(404)
            with modules.dbutils.dbopen() as db:
                db.execute("DELETE FROM games WHERE game_id={}".format(bottle.request.query.get('delete')))
                raise bottle.redirect('/games')
        if 'add' in bottle.request.query:
            if not pages.loggedin():
                raise bottle.HTTPError(404)
            with modules.dbutils.dbopen() as db:
                sports = db.execute("SELECT sport_id, title FROM sport_types")
                game_types = db.execute("SELECT type_id, sport_type, title FROM game_types")
                cities = db.execute("SELECT city_id, title FROM cities")
                courts = db.execute("SELECT court_id, city_id, title FROM courts")
                return pages.Template("addgame", sports=sports,
                                      game_types=game_types, cities=cities, courts=courts)
        if 'game_id' in bottle.request.query:
            with modules.dbutils.dbopen() as db:
                modules.dbutils.get(db).game(bottle.request.query.get('game_id'))
                if len(db.last()) == 0:
                    raise bottle.HTTPError(404)
                game = db.last()[0]
                game['city'] = modules.dbutils.get(db).city(game['city_id'])[0]
                #game['region'] = modules.dbutils.get(db).region(game['region_id'])[0]
                game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
                game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
                game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
                game.pop('city_id')
                game.pop('region_id')
                game.pop('court_id')
                modules.dbutils.strdates(game)
                game['datetime'] = (
                    beautifuldate(game['datetime']), beautifultime(game['datetime']), beautifulday(game['datetime']))
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
                #game['region'] = modules.dbutils.get(db).region(game['region_id'])[0]
                game['court'] = modules.dbutils.get(db).court(game['court_id'])[0]
                game['game_type'] = modules.dbutils.get(db).game_type(game['game_type'])[0]
                game['sport_type'] = modules.dbutils.get(db).sport_type(game['sport_type'])[0]
                game.pop('city_id')
                game.pop('region_id')
                game.pop('court_id')
                modules.dbutils.strdates(game)
                game['datetime'] = (
                beautifuldate(game['datetime']), beautifultime(game['datetime']), beautifulday(game['datetime']))
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