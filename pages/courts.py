import bottle
from modules.utils import beautifuldate, beautifultime, beautifulday

import pages
from modules import dbutils
from models import courts, games, sport_types, cities, images


class Courts(pages.Page):
    def get_court_id(self):
        court_id = int(bottle.request.query.get('court_id'))
        with dbutils.dbopen() as db:
            court = courts.get(court_id, detalized=True, dbconnection=db)
            if len(court) == 0:
                raise bottle.HTTPError(404)
            nearest_game = games.get_recent(court_id=court_id, detalized=True, count=slice(1), dbconnection=db)
            page = pages.PageBuilder('courts', court=court)
            if len(nearest_game) > 0:
                game_ = nearest_game[0]
                game_['parsed_datetime'] = (beautifuldate(game_['datetime']),
                                            beautifultime(game_['datetime']),
                                            beautifulday(game_['datetime']))
                page.add_param('game', game_)
            return page

    def get_add(self):
        with dbutils.dbopen() as db:
            _sport_types = sport_types.get(0, dbconnection=db)
            _cities = cities.get(0, dbconnection=db)
            return pages.PageBuilder('addcourt', sport_types=_sport_types, cities=_cities)

    def get_edit(self):
        with dbutils.dbopen() as db:
            court_id = int(bottle.request.query.get('edit'))
            court = courts.get(court_id, detalized=True, dbconnection=db)
            _sport_types = sport_types.get(0, dbconnection=db)
            _cities = cities.get(0, dbconnection=db)
            return pages.PageBuilder('editcourt', sport_types=_sport_types, cities=_cities, court=court)

    def get_all(self):
        with dbutils.dbopen() as db:
            city = cities.get(1, dbconnection=db)
            courts_list = courts.get(0, city_id=city['city_id'], detalized=True, dbconnection=db,
                                     fields=['court_id', 'title', 'address', 'geopoint', 'sport_types'])
        return pages.PageBuilder('courtsmap', courts=courts_list, city=city)

    def get(self):
        if 'court_id' in bottle.request.query:
            return self.get_court_id()
        if 'all' in bottle.request.query:
            return self.get_all()
        if pages.auth_dispatcher.admin():
            if 'add' in bottle.request.query:
                return self.get_add()
            if 'edit' in bottle.request.query:
                return self.get_edit()
            raise bottle.HTTPError(404)
        elif 'add' in bottle.request.query or 'edit' in bottle.request.query:
            return pages.templates.permission_denied()
        return bottle.HTTPError(404)


    def post_submit_add(self):
        if not pages.auth_dispatcher.admin():
            raise bottle.HTTPError(404)
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
            images.save_court_photo(court_id, bottle.request.files.get('photo'))
        raise bottle.redirect('/courts?court_id={}'.format(court_id))

    def post_submit_edit(self):
        if not pages.auth_dispatcher.admin():
            raise bottle.HTTPError(404)
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop('submit_edit')
        if 'photo' in params:
            params.pop('photo')
        params['sport_types'] = ','.join(bottle.request.forms.getall('sport_type'))
        params.pop('sport_type')
        params['phone'] = params['phone'] if params['phone'] else 'Не указан'
        sql = 'UPDATE courts SET {} WHERE court_id={}'.format(
            ', '.join(["{}='{}'".format(i, params[i]) for i in params]),
            params['court_id'])
        with dbutils.dbopen() as db:
            db.execute(sql)
        if 'photo' in bottle.request.files:
            images.save_court_photo(params['court_id'], bottle.request.files.get('photo'))
        raise bottle.redirect('/courts?court_id={}'.format(params['court_id']))

    def post(self):
        if 'submit_add' in bottle.request.forms and pages.auth_dispatcher.organizer():
            self.post_submit_add()
        if 'submit_edit' in bottle.request.forms and pages.auth_dispatcher.organizer():
            self.post_submit_edit()
        raise bottle.HTTPError(404)

    get.route = '/courts'
    post.route = get.route
