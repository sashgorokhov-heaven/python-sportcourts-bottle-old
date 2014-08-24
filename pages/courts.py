import os

from PIL import Image
import bottle

import pages
from modules import dbutils


class Courts(pages.Page):
    path = ['courts']

    @pages.setlogin
    def get(self):
        if 'court_id' in bottle.request.query:
            court_id = bottle.request.query.get('court_id')
            with dbutils.dbopen() as db:
                court = dbutils.get(db).court(court_id)[0]
                sport_types = list(filter(lambda x: x != '', map(lambda x: x.strip(), court['sport_types'].split(','))))
                court['sport_types'] = list()
                for sport_id in sport_types:
                    court['sport_types'].append(dbutils.get(db).sport_type(sport_id)[0])
                court['city'] = dbutils.get(db).city(court['city_id'])[0]
                court.pop('city_id')
                # court['region'] = dbutils.get(db).region(court['region_id'])[0]
                court.pop('region_id')
                sql = "SELECT game_id FROM games WHERE (city_id='{}' AND court_id='{}') AND datetime>NOW() ORDER BY datetime ASC LIMIT 1;".format(
                    court['city']['city_id'], court_id)
                db.execute(sql)
                template = pages.Template('courts', court=court)
                if len(db.last()) > 0:
                    template.add_parameter('game_id', db.last()[0][0])
                return template
        if 'add' in bottle.request.query:  # and 0 < pages.getadminlevel() <= 2:
            with dbutils.dbopen() as db:
                sport_types = db.execute("SELECT * FROM sport_types", dbutils.dbfields['sport_types'])
                cities = db.execute("SELECT * FROM cities", dbutils.dbfields['cities'])
                return pages.Template('addcourt', sport_types=sport_types, cities=cities)
        raise bottle.HTTPError(404)

    def post(self):
        if 'submit_add' in bottle.request.forms:  # and 0 < pages.getadminlevel() <= 2:
            params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
            params.pop('submit_add')
            params['sport_types'] = ','.join(bottle.request.forms.getall('sport_type'))
            params.pop('sport_type')
            params['cost'] = 1500  # FIXIT
            sql = 'INSERT INTO courts ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(params[key]) for key in keylist]))
            with dbutils.dbopen() as db:
                db.execute(sql)
                court_id = db.execute('SELECT last_insert_id() FROM games')[0][0]
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

        if 'submit_edit' in bottle.request.forms and 0 < pages.getadminlevel() <= 2:
            pass
        raise bottle.HTTPError(404)
