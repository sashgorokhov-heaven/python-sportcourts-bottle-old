import bottle
import json
import cacher

import pages
import modules
from modules import utils
import dbutils
from models import sport_types, game_types, cities, courts, games, users, notificating, reports, images


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
    utils.spool_func(notificating.site.responsible, user_id, notification, 2, game_id)

def unassigned_responsible(game_id:int, user_id:int, db):
    if user_id == pages.auth.current().user_id():
        return
    game = games.get_by_id(game_id, dbconnection=db)
    notification = 'Вы больше не являетесь ответственным за игру "{}".'
    notification = notification.format(modules.create_link.game(game))
    utils.spool_func(notificating.site.responsible, user_id, notification, 2, game_id)


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
                utils.spool_func(notificating.site.subscribed, user_id, 'Игра "{}" была отредактирована.<br>Проверьте изменения!'.format(
                    modules.create_link.game(game)), 1, game_id)
            if responsible_old == int(params['responsible_user_id']):
                utils.spool_func(notificating.site.responsible, responsible_old, 'Игра "{}" была отредактирована.<br>Проверьте изменения!'.format(
                    modules.create_link.game(game)), 1, game_id)
        raise bottle.redirect('/games/{}'.format(game_id))


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
                                     description='В это время уже идет другая <a href="/games/{}">игра</a>'.format(
                                         intersection))
        page = check_responsible(params['responsible_user_id'], params['datetime'],
                                      params['duration'].split(' ')[0], db)
        if page: return page
        if int(params['capacity']) > 0:
            params['reserved'] = round(int(params['capacity']) / 4)
        game_id = games.add(dbconnection=db, **params)
        assigned_responsible(game_id, int(params['responsible_user_id']), db)
        return bottle.redirect('/games/{}'.format(game_id))


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


@pages.get('/games/notify/<game_id:int>')
@pages.only_ajax
@pages.only_organizers
def notify(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        db.execute("SELECT DISTINCT user_id FROM reports WHERE user_id!=0 AND status=2 AND game_id IN (SELECT game_id FROM games WHERE deleted=0 AND datetime+INTERVAL duration MINUTE < NOW() AND court_id='{}' AND sport_type='{}' AND game_type='{}')".format( # as long as my dick
            game.court_id(), game.sport_type(), game.game_type()))
        if len(db.last())==0: return json.dumps({'users':list(), 'count':0})
        users_ = users.get(list(map(lambda x: x[0], db.last())), dbconnection=db)
        for user in users_:
            utils.spool_func(notificating.mail.tpl.game_invite, game, user)
        ids = list(map(lambda x: x.user_id(), users_))
        return json.dumps({'count':len(ids), 'users':ids})


@pages.get('/games/report/<game_id:int>')
@pages.only_organizers
def get_report(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)
        if len(game) == 0:
            raise bottle.HTTPError(404)
        if game.created_by() != pages.auth.current().user_id() and game.responsible_user_id() != pages.auth.current().user_id() and not pages.auth.current().userlevel.admin():
            return pages.templates.permission_denied()
        if not game.datetime.passed:
            return pages.templates.message("Вы не можете отправить отчет по игре", "Игра еще не закончилась")
        return pages.PageBuilder("report", game=game, showreport=game.reported())


@pages.post('/games/report/<game_id:int>')
@pages.only_organizers
def post(game_id:int):
    game = games.get_by_id(game_id)
    if game.created_by() != pages.auth.current().user_id() and game.responsible_user_id() != pages.auth.current().user_id() and not pages.auth.current().userlevel.admin():
        return pages.templates.permission_denied()
    if game.reported(): return pages.templates.message('Чё', 'Эээ')
    users_ = {int(user_id.split('=')[-1]): {"status": bottle.request.forms.get(user_id)} for user_id in
              filter(lambda x: x.startswith("status"), bottle.request.forms)}
    registered = {user_id: users_[user_id] for user_id in filter(lambda x: x > 0, users_)}
    unregistered = {user_id: users_[user_id] for user_id in filter(lambda x: x < 0, users_)}
    for user_id in unregistered:
        info = {key.split('=')[0]: bottle.request.forms.get(key) for key in
                filter(lambda x: x.endswith(str(user_id)), bottle.request.forms)}
        unregistered[user_id] = info
    report = dict()
    report['registered'] = {'count': len(registered), 'users': registered}
    report['unregistered'] = {'count': len(unregistered), 'users': unregistered}
    report['additional_charges'] = {int(i.split('=')[1]):(bottle.request.forms.get(i), bottle.request.forms.get('amount'+i.split('=')[1])) for i in filter(lambda x: x.startswith('description'), bottle.request.forms)}
    with dbutils.dbopen() as db:
        for user_id in report['unregistered']['users']:
            user = report['unregistered']['users'][user_id]
            name = user['first_name'].strip()+' '+user['last_name'].strip()
            reports.report_unregistered(game_id, user['status'], name, user['phone'], dbconnection=db)
        for user_id in report['registered']['users']:
            user = report['registered']['users'][user_id]
            status = user['status']
            reports.report(game_id, user_id, status, dbconnection=db)
        for n in report['additional_charges']:
            reports.report_additional_charges(game_id, *report['additional_charges'][n], dbconnection=db)
    if "photo" in bottle.request.files:
        images.save_report(game_id, bottle.request.files.get("photo"))
    if pages.auth.current().user_id() != game.created_by():
        notificating.site.responsible(game.created_by(), 'Ответственный "{}" отправил отчет по игре "{}"'.format(
            modules.create_link.user(users.get(pages.auth.current().user_id())),
            modules.create_link.game(game)), game_id)
    cacher.drop_by_table_name('games', 'game_id', game_id)
    raise bottle.redirect('/games/report/{}'.format(game_id))


@pages.get("/games/autocreate/<game_id:int>")
@pages.only_organizers
def autocreate(game_id:int):
    with dbutils.dbopen() as db:
        game = games.get_by_id(game_id, dbconnection=db)