import os

from PIL import Image
import bottle

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
            template = pages.Template('courts', court=court)
            if len(db.last()) > 0:
                template.add_parameter('game_id', db.last()[0][0])
            return template

    def get_add(self):
        with dbutils.dbopen() as db:
            sport_types = db.execute("SELECT * FROM sport_types", dbutils.dbfields['sport_types'])
            cities = db.execute("SELECT * FROM cities", dbutils.dbfields['cities'])
            return pages.Template('addcourt', sport_types=sport_types, cities=cities)

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

            return pages.Template('editcourt', sport_types=sport_types, cities=cities, court=court)

    @pages.setlogin
    def get(self):
        if 'court_id' in bottle.request.query:
            return self.get_court_id()
        if 'add' in bottle.request.query and 0 < pages.getadminlevel() <= 2:
            return self.get_add()
        if 'edit' in bottle.request.query and 0 < pages.getadminlevel() <= 2:
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
        params['cost'] = 1500  # FIXIT
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
        params['cost'] = 1500  # FIXIT
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
        if 'submit_add' in bottle.request.forms and 0 < pages.getadminlevel() <= 2:
            self.post_submit_add()

        if 'submit_edit' in bottle.request.forms and 0 < pages.getadminlevel() <= 2:
            self.post_submit_edit()
        raise bottle.HTTPError(404)

    get.route = '/courts'
    post.route = get.route
