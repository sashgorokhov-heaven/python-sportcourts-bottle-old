import bottle

import pages
import modules
from modules.utils import beautifuldate, beautifulday, beautifultime
import modules.dbutils
from models import sport_types, game_types, cities, courts, games, notifications, users


GAMES_PER_PAGE = 4


class Games(pages.Page):
    def check_responsible(self, user_id:int, datetime:str, duration:int, db):
        query = """\
          SELECT game_id FROM games WHERE responsible_user_id={user_id} AND (\
          (DATETIME BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE) OR \
          (DATETIME + INTERVAL {duration} MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE));\
          """.format(user_id=user_id, datetime=datetime, duration=duration)
        db.execute(query)
        if len(db.last()) != 0:
            return pages.templates.message("{} уже занят на это время".format(
                modules.create_link.user(
                    users.get(
                        int(params['responsible_user_id']),
                        fields=['user_id', 'first_name', 'last_name'],
                        dbconnection=db))), '')

    def assigned_responsible(self, game_id:int, user_id:int, db):
        if user_id == pages.auth_dispatcher.getuserid():
            return
        game = games.get_by_id(game_id, fields=['game_id', 'description', 'created_by'], dbconnection=db)
        created_by = users.get(game['created_by'], fields=['user_id', 'first_name', 'last_name'])
        notification = 'Вас назначили ответственным на игру "{}"<br>Свяжитесь с "{}"!'
        notification = notification.format(modules.create_link.game(game), modules.create_link.user(created_by))
        notifications.add(user_id, notification, 2, game_id, 2, dbconnection=db)

    def unassigned_responsible(self, game_id:int, user_id:int, db):
        if user_id == pages.auth_dispatcher.getuserid():
            return
        game = games.get_by_id(game_id, fields=['game_id', 'description', 'created_by'], dbconnection=db)
        created_by = users.get(game['created_by'], fields=['user_id', 'first_name', 'last_name'])
        notification = 'Вы больше не являетесь ответсвенным за игру "{}".'
        notification = notification.format(modules.create_link.game(game), modules.create_link.user(created_by))
        notifications.add(user_id, notification, 2, game_id, dbconnection=db)

    def post_submit_add(self):
        with modules.dbutils.dbopen() as db:
            params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
            params.pop('submit_add')
            params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
            params.pop('date')
            params.pop('time')
            params['created_by'] = pages.auth_dispatcher.getuserid()
            intersection = games.intersection(params['court_id'],
                                              params['datetime'],
                                              params['duration'].encode().split(b' ')[0].decode(),
                                              dbconnection=db)
            if intersection != 0:
                return pages.PageBuilder('text', message='Обнаружен конфликт',
                                         description='В это время уже идет другая <a href="/games?game_id={}">игра</a>'.format(
                                             intersection))
            page = self.check_responsible(params['responsible_user_id'], params['datetime'],
                                          params['duration'].split(' ')[0], db)
            if page: return page
            game_id = games.add(dbconnection=db, **params)
            self.assigned_responsible(game_id, int(params['responsible_user_id']), db)
            return bottle.redirect('/games?game_id={}'.format(game_id))

    def post_submit_edit(self):
        with modules.dbutils.dbopen() as db:
            params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
            params.pop('submit_edit')
            params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
            params.pop('date')
            params.pop('time')
            game_id = int(params['game_id'])
            params.pop('game_id')
            responsible_old = games.get_by_id(game_id, fields=['responsible_user_id'], dbconnection=db)[
                'responsible_user_id']

            page = self.check_responsible(params['responsible_user_id'], params['datetime'],
                                          params['duration'].split(' ')[0], db)
            if page: return page

            if responsible_old != int(params['responsible_user_id']):
                self.assigned_responsible(game_id, int(params['responsible_user_id']), db)
                self.unassigned_responsible(game_id, responsible_old, db)
            games.update(game_id, dbconnection=db, **params)
            game = games.get_by_id(game_id, detalized=True, fields=['game_id', 'subscribed', 'description'],
                                   dbconnection=db)
            for user in game['subscribed']['users']:
                notifications.add(user['user_id'], 'Игра "{}" была отредактирована.<br>Проверьте изменения!'.format(
                    modules.create_link.game(game)), 1, game_id, 1, dbconnection=db)
            raise bottle.redirect('/games?game_id={}'.format(game_id))

    def post(self):
        if not pages.auth_dispatcher.organizer() and not pages.auth_dispatcher.admin() and not pages.auth_dispatcher.responsible():
            return pages.templates.permission_denied()
        if 'submit_add' in bottle.request.forms and not pages.auth_dispatcher.responsible():
            return self.post_submit_add()
        if 'submit_edit' in bottle.request.forms:
            return self.post_submit_edit()
        raise bottle.HTTPError(404)

    def get_edit(self):
        with modules.dbutils.dbopen() as db:
            game_id = int(bottle.request.query.get('edit'))
            game = games.get_by_id(game_id, detalized=True, dbconnection=db)
            if len(game) == 0:
                raise bottle.HTTPError(404)
            if pages.auth_dispatcher.getuserid() != game['created_by']['user_id'] and \
                            pages.auth_dispatcher.getuserid() != game['responsible_user']['user_id'] and \
                    not pages.auth_dispatcher.admin():
                return pages.templates.permission_denied()
            _sport_types = sport_types.get(0, dbconnection=db)
            _game_types = game_types.get(0, dbconnection=db)
            _cities = cities.get(0, dbconnection=db)
            _courts = courts.get(0, fields=['court_id', 'city_id', 'title'], dbconnection=db)
            responsibles = users.get(0, 2, fields=['user_id', 'first_name', 'last_name'], dbconnection=db)
            return pages.PageBuilder('editgame', game=game, sports=_sport_types, game_types=_game_types, cities=_cities,
                                     courts=_courts, responsibles=responsibles)

    def get_add(self):
        with modules.dbutils.dbopen() as db:
            _sports = sport_types.get(0, dbconnection=db)
            _game_types = game_types.get(0, dbconnection=db)
            _cities = cities.get(0, dbconnection=db)
            _courts = courts.get(0, fields=['court_id', 'city_id', 'title'], dbconnection=db)
            responsibles = users.get(0, 2, fields=['user_id', 'first_name', 'last_name'], dbconnection=db)
            return pages.PageBuilder("addgame", sports=_sports, game_types=_game_types, cities=_cities, courts=_courts,
                                     responsibles=responsibles)

    def get_game_id(self):
        with modules.dbutils.dbopen() as db:
            game_id = int(bottle.request.query.get('game_id'))
            if not game_id:
                raise bottle.HTTPError(404)
            game = games.get_by_id(game_id, detalized=True, dbconnection=db)
            if len(game) == 0:
                raise bottle.HTTPError(404)
            game['parsed_datetime'] = (beautifuldate(game['datetime'], True),
                                       beautifultime(game['datetime']),
                                       beautifulday(game['datetime']))
            if len(game) == 0:
                return bottle.HTTPError(404)
            if pages.auth_dispatcher.loggedin() \
                    and pages.auth_dispatcher.getuserid() in {user['user_id'] for user in game['subscribed']['users']}:
                game['is_subscribed'] = True
            else:
                game['is_subscribed'] = False
            return pages.PageBuilder('game', game=game, standalone=True)

    def get_page(self, page_n:int=1, sport_type:int=0):
        with modules.dbutils.dbopen() as db:
            count = len(games.get_recent(sport_type=sport_type,
                                         count=slice(0, 99999),
                                         detalized=False,
                                         fields=['game_id'],
                                         dbconnection=db))
            total_pages = count // GAMES_PER_PAGE + (1 if 0 <= count <= GAMES_PER_PAGE else 0)

            if page_n > total_pages:
                if not bottle.request.is_ajax:
                    raise bottle.HTTPError(404)
                else:
                    return {"stop": True, "games": list()}

            sports = sport_types.get(0, dbconnection=db)

            if not count:
                if not bottle.request.is_ajax:
                    return pages.PageBuilder("games", games=list(), sports=sports, bysport=sport_type)
                else:
                    return {"stop": True, "games": list()}

            allgames = games.get_recent(sport_type=sport_type,
                                        count=slice(*modules.pager(page_n, count=GAMES_PER_PAGE)), detalized=True,
                                        dbconnection=db)
            for game in allgames:
                if pages.auth_dispatcher.loggedin() \
                        and pages.auth_dispatcher.getuserid() in {user['user_id'] for user in
                                                                  game['subscribed']['users']}:
                    game['is_subscribed'] = True
                else:
                    game['is_subscribed'] = False
                game['parsed_datetime'] = (beautifuldate(game['datetime'], True),
                                           beautifultime(game['datetime']),
                                           beautifulday(game['datetime']))
            if not bottle.request.is_ajax:
                page = pages.PageBuilder('games', games=allgames, sports=sports, bysport=sport_type)
                if page_n < total_pages:
                    page.add_param("nextpage", page_n + 1)
                return page
            else:
                data = {"stop": page_n >= total_pages, "games": list()}
                page = pages.PageBuilder("game", tab_name="all")
                for game in allgames:
                    page.add_param("game", game)
                    game_tpl = page.template()
                    data["games"].append(game_tpl)
                return data

    def get_delete(self, game_id:int):
        game = games.get_by_id(game_id, fields=['created_by'])
        if game['created_by'] != pages.auth_dispatcher.getuserid() and not pages.auth_dispatcher.admin():
            return pages.templates.permission_denied()
        games.delete(game_id)
        raise bottle.redirect('/games')

    def get(self):
        if 'delete' in bottle.request.query:
            if not pages.auth_dispatcher.admin() and not pages.auth_dispatcher.organizer():
                return pages.templates.permission_denied()
            return self.get_delete(int(bottle.request.query.get('delete')))
        if 'add' in bottle.request.query:
            if pages.auth_dispatcher.organizer() or pages.auth_dispatcher.admin():
                return self.get_add()
            else:
                return pages.templates.permission_denied()
        if 'edit' in bottle.request.query:
            return self.get_edit()
        if 'game_id' in bottle.request.query:
            return self.get_game_id()
        if 'sport_id' in bottle.request.query:
            if 'page' in bottle.request.query:
                return self.get_page(int(bottle.request.query.get('page')), int(bottle.request.query.get('sport_id')))
            else:
                return self.get_page(1, int(bottle.request.query.get('sport_id')))
        if 'page' in bottle.request.query and 'sport_id' not in bottle.request.query:
            return self.get_page(int(bottle.request.query.get('page')))
        return self.get_page(1)

    get.route = '/games'
    post.route = get.route