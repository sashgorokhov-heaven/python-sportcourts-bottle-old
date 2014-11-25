import bottle

import pages
import modules
import dbutils
from models import sport_types, game_types, cities, courts, games, notifications, users


GAMES_PER_PAGE = 4


def check_responsible(user_id:int, datetime:str, duration:int, db):
    query = """\
         SELECT game_id FROM games WHERE responsible_user_id={user_id} AND (\
         (DATETIME BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE) OR \
         (DATETIME + INTERVAL {duration} MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE));\
         """.format(user_id=user_id, datetime=datetime, duration=duration)
    db.execute(query)
    if len(db.last()) != 0:
        return pages.templates.message("{} уже занят на это время".format(
            modules.create_link.user(users.get(user_id, dbconnection=db))), '')

def assigned_responsible(game_id:int, user_id:int, db):
    if user_id == pages.auth.current().user_id():
        return
    game = games.get_by_id(game_id, dbconnection=db)
    notification = 'Вас назначили ответственным на игру "{}"<br>Свяжитесь с "{}"!'
    notification = notification.format(modules.create_link.game(game),
                                       modules.create_link.user(game.created_by(True)))
    notifications.add(user_id, notification, 2, game_id, 2)

def unassigned_responsible(game_id:int, user_id:int, db):
    if user_id == pages.auth.current().user_id():
        return
    game = games.get_by_id(game_id, dbconnection=db)
    notification = 'Вы больше не являетесь ответственным за игру "{}".'
    notification = notification.format(modules.create_link.game(game))
    notifications.add(user_id, notification, 2, game_id, 2)


@pages.get('/games/<game_id:int>')
def get_by_id(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if len(game) == 0:
            raise bottle.HTTPError(404)
        return pages.PageBuilder('game', game=game, standalone=True)


@pages.get('/games/delete/<game_id:int>')
@pages.only_organizers
def delete(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if game.created_by() != pages.auth.current().user_id() and not pages.auth.current().userlevel.admin():
            return pages.templates.permission_denied()
        games.delete(game_id, dbconnection=db)
        raise bottle.redirect('/games')


@pages.get('/games/edit/<game_id:int>')
@pages.only_organizers
def edit(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if len(game) == 0:
            raise bottle.HTTPError(404)
        if pages.auth.current().user_id() != game.created_by() and \
                        pages.auth.current().user_id() != game.responsible_user_id() and \
                not pages.auth.current().userlevel.admin():
            return pages.templates.permission_denied()
        _sport_types = sport_types.get(0, dbconnection=db)
        _game_types = game_types.get(0, dbconnection=db)
        _cities = cities.get(0, dbconnection=db)
        _courts = courts.get(0, dbconnection=db)
        responsibles = users.get(0, 2, dbconnection=db)
        return pages.PageBuilder('editgame', game=game, sports=_sport_types, game_types=_game_types, cities=_cities,
                                 courts=_courts, responsibles=responsibles)


@pages.post('/games/edit/<game_id:int>')
@pages.only_organizers
def edit_post(game_id:int):
    with dbutils.dbopen() as db:
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop('submit_edit')
        params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
        params.pop('date')
        params.pop('time')
        params.pop('game_id')
        responsible_old = games.get_by_id(game_id, dbconnection=db).responsible_user_id()
        if responsible_old != int(params['responsible_user_id']):
            page = check_responsible(params['responsible_user_id'], params['datetime'],
                                          params['duration'].split(' ')[0], db)
            if page: return page
            assigned_responsible(game_id, int(params['responsible_user_id']), db)
            unassigned_responsible(game_id, responsible_old, db)
        games.update(game_id, dbconnection=db, **params)
        game = games.get_by_id(game_id, dbconnection=db)
        if not game.datetime.passed:
            for user_id in game.subscribed():
                notifications.add(user_id, 'Игра "{}" была отредактирована.<br>Проверьте изменения!'.format(
                    modules.create_link.game(game)), 1, game_id, 1)
            if responsible_old == int(params['responsible_user_id']):
                notifications.add(responsible_old, 'Игра "{}" была отредактирована.<br>Проверьте изменения!'.format(
                    modules.create_link.game(game)), 1, game_id, 2)
        raise bottle.redirect('/games?game_id={}'.format(game_id))


@pages.get('/games/add')
@pages.only_organizers
def add():
    with dbutils.dbopen() as db:
        _sports = sport_types.get(0, dbconnection=db)
        _game_types = game_types.get(0, dbconnection=db)
        _cities = cities.get(0, dbconnection=db)
        _courts = courts.get(0, dbconnection=db)
        responsibles = users.get(0, 2, dbconnection=db)
        return pages.PageBuilder("addgame", sports=_sports, game_types=_game_types, cities=_cities, courts=_courts,
                                 responsibles=responsibles)


@pages.post('/games/add')
@pages.only_organizers
def add_post():
    with dbutils.dbopen() as db:
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop('submit_add')
        params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
        params.pop('date')
        params.pop('time')
        params['created_by'] = pages.auth.current().user_id()
        intersection = games.court_game_intersection(params['court_id'],
                                                     params['datetime'],
                                                     params['duration'].encode().split(b' ')[0].decode(),
                                                     dbconnection=db)
        if intersection:
            return pages.PageBuilder('text', message='Обнаружен конфликт',
                                     description='В это время уже идет другая <a href="/games?game_id={}">игра</a>'.format(
                                         intersection))
        page = check_responsible(params['responsible_user_id'], params['datetime'],
                                      params['duration'].split(' ')[0], db)
        if page: return page
        if int(params['capacity']) > 0:
            params['reserved'] = round(int(params['capacity']) / 4)
        game_id = games.add(dbconnection=db, **params)
        assigned_responsible(game_id, int(params['responsible_user_id']), db)
        return bottle.redirect('/games?game_id={}'.format(game_id))


@pages.get('/games/list/<game_id:int>')
@pages.only_organizers
def subscribed_list(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if len(game) == 0:
            raise bottle.HTTPError(404)
        if pages.auth.current().user_id() != game.created_by() and pages.auth.current().user_id() != game.responsible_user_id() and not pages.auth.current().userlevel.admin():
            return pages.templates.permission_denied()
        return pages.PageBuilder('list', game=game)


@pages.get('/games')
def get():
    def _get_games(*args):
        ptype = args[0]
        sport_type = 0
        page_n = 1

        if ptype == 'all' or ptype == 'old':
            page_n = args[1]
        elif ptype == 'sport':
            sport_type = args[1]
            page_n = args[2]

        with dbutils.dbopen() as db:
            count = len(games.get_recent(sport_type=sport_type,
                                         count=slice(0, 99999),
                                         old=ptype == 'old',
                                         dbconnection=db))  # TODO: REWORK
            total_pages = count // GAMES_PER_PAGE + (1 if count % GAMES_PER_PAGE != 0 else 0)
            if page_n > total_pages and count>0:
                if not bottle.request.is_ajax:
                    raise bottle.HTTPError(404)
                else:
                    return {"stop": True, "games": list()}

            sports = sport_types.get(0, dbconnection=db)

            if not count:
                if not bottle.request.is_ajax:
                    return pages.PageBuilder("games", games=list(), sports=sports, bysport=sport_type,
                                             old=ptype == 'old')
                else:
                    return {"stop": True, "games": list()}

            allgames = games.get_recent(sport_type=sport_type, old=ptype == 'old',
                                        count=slice(*modules.pager(page_n, count=GAMES_PER_PAGE)), dbconnection=db)

            if not bottle.request.is_ajax:
                return pages.PageBuilder('games', games=allgames, sports=sports, bysport=sport_type, old=ptype == 'old')
            else:
                data = {"stop": page_n >= total_pages, "games": list()}
                page = pages.PageBuilder("game", tab_name="all")
                for game in allgames:
                    page.add_param("game", game)
                    game_tpl = page.template()
                    data["games"].append(game_tpl)
                return data

    def get_all(page_n:int=1):
        return _get_games('all', page_n)

    def get_by_sport(sport_id:int, page_n:int=1):
        return _get_games('sport', sport_id, page_n)

    def get_old(page_n:int=1):
        return _get_games('old', page_n)

    if 'sport_id' in bottle.request.query:
        return get_by_sport(int(bottle.request.query.get('sport_id')),
                            int(bottle.request.query.get('page')) if 'page' in bottle.request.query else 1)
    if 'old' in bottle.request.query:
        return get_old(int(bottle.request.query.get('page')) if 'page' in bottle.request.query else 1)
    return get_all(int(bottle.request.query.get('page')) if 'page' in bottle.request.query else 1)


@pages.post('/games')
def post():
    pass