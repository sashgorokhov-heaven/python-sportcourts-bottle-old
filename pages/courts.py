import bottle

import dbutils
import pages
from models import courts, games, sport_types, cities, images, court_types


def get_courts_map():
    with dbutils.dbopen() as db:
        city = cities.get(1, dbconnection=db)
        courts_list = courts.get(0, city_id=city.city_id(), dbconnection=db)
        _games = games.get_recent(dbconnection=db)
        colors = ['redPoint', 'greenPoint', 'bluePoint', 'yellowPoint', 'orangePoint', 'darkbluePoint', 'greyPoint',
                  'whitePoint', 'lightbluePoint']
        court_games = {court.court_id(): list(filter(lambda x: x.court_id() == court.court_id(), _games)) for court
                       in courts_list}
        _sport_types = {sport_type.title(): sport_type for court in courts_list for sport_type in
                        court.sport_types(True)}
        group_string = 'createGroup("{title}", [{courts}], "default#{color}")'
        court_string = 'createPlacemark(new YMaps.GeoPoint({geopoint}), "{title} <br> {address}", "<a href=\'/courts/{court_id}\' target=\'_blank\'>Подробнее...</a>")'
        games_string = '<br><br>Ближайшие игры:'
        game_string = '<br>{n}. <a href=\'/games/{game_id}\' target=\'_blank\'>{datetime} | {sport_type} - {game_type}</a>'

        def create_group(courts:list, color_n:int, name:str) -> str:
            court_strings = []
            for court in courts:
                court_string_f = court_string.format(geopoint=court.geopoint(),
                                                     title='\\"'.join(court.title().split('"')),
                                                     address=','.join(court.address().split(',')[-3:]),
                                                     court_id=court.court_id())
                if len(court_games[court.court_id()]) > 0:
                    court_string_f = court_string_f[:-2] + games_string
                    for n, game in enumerate(court_games[court.court_id()], 1):
                        court_string_f += game_string.format(
                            datetime=game.datetime.beautiful,
                            sport_type=game.sport_type(True).title(),
                            game_type=game.game_type(True).title(),
                            game_id=game.game_id(),
                            n=n)
                    court_string_f += '")'
                court_string_f = court_string_f[:-1]
                court_string_f += ',' + ('false', 'true')[len(list(
                    filter(lambda x: x.sport_type(True).title() == name,
                           court_games[court.court_id()])) if name != 'Все' else court_games[court.court_id()]) > 0]
                dic = {game.sport_type(): game.sport_type(True).title() for game in court_games[court.court_id()]}
                court_string_f += ', [{}]'.format(
                    ','.join(['[{}, "{}"]'.format(sport_type_id, dic[sport_type_id]) for sport_type_id in dic]))
                court_string_f += ')'
                court_strings.append(court_string_f)
            return group_string.format(title=name, courts=','.join(court_strings), color=colors[color_n])

        groups = [create_group(courts_list, -1, 'Все')]

        for n, sport_type_title in enumerate(_sport_types):
            sport_type = _sport_types[sport_type_title]
            court_list = [court for court in courts_list if
                          sport_type.title() in {sport_type.title() for sport_type in court.sport_types(True)}]
            groups.append(create_group(court_list, n, sport_type_title))

        return pages.PageBuilder('courtsmap', groups=groups, city=city)


@pages.get('/courts/<court_id:int>')
def get_by_id(court_id:int):
    with dbutils.dbopen() as db:
        court = courts.get(court_id, dbconnection=db)
        if not court:
            raise bottle.HTTPError(404)
        return pages.PageBuilder('courts', court=court)


@pages.get('/courts/add')
@pages.only_admins
def add():
    with dbutils.dbopen() as db:
        _sport_types = sport_types.get(0, dbconnection=db)
        _cities = cities.get(0, dbconnection=db)
        _court_types = court_types.get(0, dbconnection=db)
        return pages.PageBuilder('addcourt', sport_types=_sport_types, cities=_cities, court_types=_court_types)


@pages.post('/courts/add')
@pages.only_admins
def add_post():
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
    raise bottle.redirect('/courts/{}'.format(court_id))


@pages.get('/courts/edit/<court_id:int>')
@pages.only_organizers
def edit(court_id:int):
    with dbutils.dbopen() as db:
        court = courts.get(court_id, dbconnection=db)
        _sport_types = sport_types.get(0, dbconnection=db)
        _cities = cities.get(0, dbconnection=db)
        _court_types = court_types.get(0, dbconnection=db)
        return pages.PageBuilder('editcourt', sport_types=_sport_types, cities=_cities, court=court,
                                 court_types=_court_types)


@pages.post('/courts/edit/<court_id:int>')
@pages.only_organizers
def edit_post(court_id:int):
    params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
    params.pop('submit_edit')
    if 'photo' in params:
        params.pop('photo')
    params['sport_types'] = ','.join(bottle.request.forms.getall('sport_type'))
    params.pop('sport_type')
    params['phone'] = params['phone'] if params['phone'] else 'Не указан'
    sql = 'UPDATE courts SET {} WHERE court_id={}'.format(
        ', '.join(["{}='{}'".format(i, params[i]) for i in params]),
        court_id)
    with dbutils.dbopen() as db:
        db.execute(sql)
    if 'photo' in bottle.request.files:
        images.save_court_photo(court_id, bottle.request.files.get('photo'))
    raise bottle.redirect('/courts/{}'.format(court_id))


@pages.get('/courts')
def get():
    if 'court_id' in bottle.request.query:
        raise bottle.redirect('/courts/{}'.format(bottle.request.get('court_id')))
    return get_courts_map()