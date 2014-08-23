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
                db.execute(
                    "SELECT game_id FROM games WHERE city_id=1 AND datetime>NOW() ORDER BY datetime ASC LIMIT 1;")
                template = pages.Template('courts', court=court)
                if len(db.last()) > 0:
                    template.add_parameter('game_id', db.last()[0][0])
                return template
        if 'add' in bottle.request.query and 0 < pages.getadminlevel() <= 2:
            with dbutils.dbopen() as db:
                sport_types = db.execute("SELECT * FROM sport_types", dbutils.dbfields['sport_types'])
                cities = db.execute("SELECT * FROM cities", dbutils.dbfields['cities'])
                return pages.Template('addcourt', sport_types=sport_types, cities=cities)
        raise bottle.HTTPError(404)

    def post(self):
        if 'submit_add' in bottle.request.forms and 0 < pages.getadminlevel() <= 2:
            pass
        raise bottle.HTTPError(404)
