import os

from PIL import Image
import bottle

from modules.utils import beautifuldate, beautifultime, beautifulday
import pages
from modules import dbutils


class Courts(pages.Page):
    def get_court_id(self):
        court_id = bottle.request.query.get('court_id')
        with dbutils.dbopen() as db:
            court = dbutils.get(db).court(court_id)[0]
            sport_types = list(filter(lambda x: x != '', map(lambda x: x.strip(), court['sport_types'].split(','))))
            court['sport_types'] = list()
            for sport_id in sport_types:
                court['sport_types'].append(dbutils.get(db).sport_type(sport_id)[0])
            court['city'] = dbutils.get(db).city(court['city_id'])[0]
            court.pop('city_id')
            sql = "SELECT game_id FROM games WHERE (city_id='{}' AND court_id='{}') AND datetime>NOW() ORDER BY datetime ASC LIMIT 1;".format(
                court['city']['city_id'], court_id)
            db.execute(sql)
            page = pages.PageBuilder('courts', court=court)
            if len(db.last()) > 0:
                page.add_param('game', self.get_game_by_id(db, db.last()[0][0]))
            return page

    def get_game_by_id(self, db, game_id:int) -> dict:
        game = dbutils.get(db).game(game_id)[0]
        game['city'] = dbutils.get(db).city(game['city_id'])[0]
        game['court'] = dbutils.get(db).court(game['court_id'])[0]
        game['game_type'] = dbutils.get(db).game_type(game['game_type'])[0]
        game['sport_type'] = dbutils.get(db).sport_type(game['sport_type'])[0]
        game.pop('city_id')
        game.pop('court_id')
        dbutils.strdates(game)
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
        return game

    def get_add(self):
        with dbutils.dbopen() as db:
            sport_types = db.execute("SELECT * FROM sport_types", dbutils.dbfields['sport_types'])
            cities = db.execute("SELECT * FROM cities", dbutils.dbfields['cities'])
            return pages.PageBuilder('addcourt', sport_types=sport_types, cities=cities)

    def get_edit(self):
        with dbutils.dbopen() as db:
            court_id = bottle.request.query.get('edit')
            court = dbutils.get(db).court(court_id)[0]
            sport_types = db.execute("SELECT * FROM sport_types", dbutils.dbfields['sport_types'])
            cities = db.execute("SELECT * FROM cities", dbutils.dbfields['cities'])
            court_sport_types = list(
                filter(lambda x: x != '', map(lambda x: x.strip(), court['sport_types'].split(','))))
            court['sport_types'] = list()
            for sport_id in court_sport_types:
                court['sport_types'].append(dbutils.get(db).sport_type(sport_id)[0])
            court['city'] = dbutils.get(db).city(court['city_id'])[0]
            court.pop('city_id')
            return pages.PageBuilder('editcourt', sport_types=sport_types, cities=cities, court=court)

    def get(self):
        if 'court_id' in bottle.request.query:
            return self.get_court_id()
        if 'add' in bottle.request.query and pages.auth_dispatcher.organizer():
            return self.get_add()
        if 'edit' in bottle.request.query and pages.auth_dispatcher.organizer():
            return self.get_edit()
        raise bottle.HTTPError(404)

    def post_submit_add(self):
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop('submit_add')
        if 'photo' in params:
            params.pop('photo')
        params['sport_types'] = ','.join(bottle.request.forms.getall('sport_type'))
        params.pop('sport_type')
        params['phone'] = params['phone'] if params['phone'] else 'Не указан'
        sql = 'INSERT INTO courts ({dbkeylist}) VALUES ({dbvaluelist})'
        keylist = list(params.keys())
        sql = sql.format(
            dbkeylist=', '.join(keylist),
            dbvaluelist=', '.join(["'{}'".format(params[key]) for key in keylist]))
        with dbutils.dbopen() as db:
            db.execute(sql)
            court_id = db.execute('SELECT last_insert_id() FROM courts')[0][0]
        if 'photo' in bottle.request.files:
            filename = str(court_id) + '.jpg'
            dirname = '/bsp/data/images/courts/'
            fullname = os.path.join(dirname, filename)
            if os.path.exists(fullname):
                os.remove(fullname)
            bottle.request.files.get('photo').save(fullname)
            im = Image.open(fullname)
            im.save(fullname)
            im.close()
        raise bottle.redirect('/courts?court_id={}'.format(court_id))

    def post_submit_edit(self):
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop('submit_edit')
        if 'photo' in params:
            params.pop('photo')
        params['sport_types'] = ','.join(bottle.request.forms.getall('sport_type'))
        params.pop('sport_type')
        params['phone'] = params['phone'] if params['phone'] else 'Не указан'
        sql = 'UPDATE courts SET {} WHERE court_id={}'.format(
            ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
            params['court_id'])
        with dbutils.dbopen() as db:
            db.execute(sql)
        if 'photo' in bottle.request.files:
            filename = str(params['court_id']) + '.jpg'
            dirname = '/bsp/data/images/courts/'
            fullname = os.path.join(dirname, filename)
            if os.path.exists(fullname):
                os.remove(fullname)
            bottle.request.files.get('photo').save(fullname)
            im = Image.open(fullname)
            im.save(fullname)
            im.close()
        raise bottle.redirect('/courts?court_id={}'.format(params['court_id']))

    def post(self):
        if 'submit_add' in bottle.request.forms and pages.auth_dispatcher.organizer():
            self.post_submit_add()
        if 'submit_edit' in bottle.request.forms and pages.auth_dispatcher.organizer():
            self.post_submit_edit()
        raise bottle.HTTPError(404)

    get.route = '/courts'
    post.route = get.route
