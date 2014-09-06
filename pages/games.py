import bottle

import pages
import modules
import modules.dbutils
from models import sport_types, game_types, cities, courts, games, notifications


GAMES_PER_PAGE = 20


class Games(pages.Page):
    def post_submit_add(self):
        with modules.dbutils.dbopen() as db:
            params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
            params.pop('submit_add')
            params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
            params.pop('date')
            params.pop('time')
            intersection = games.intersection(params['court_id'],
                                              params['datetime'],
                                              params['duration'].encode().split(b' ')[0].decode(),
                                              dbconnection=db)
            if intersection != 0:
                return pages.PageBuilder('text', message='Обнаружен конфликт',
                                         description='В это время уже идет другая <a href="/games?game_id={}">игра</a>'.format(
                                             intersection))
            game_id = games.add(dbconnection=db, **params)
            return bottle.redirect('/games?game_id={}'.format(game_id))

    def post_submit_edit(self):
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop('submit_edit')
        params['datetime'] = params['date'] + ' ' + params['time'] + ':00'
        params.pop('date')
        params.pop('time')
        game_id = int(params['game_id'])
        params.pop('game_id')
        games.update(game_id, **params)
        game = games.get_by_id(game_id, detalized=True, fields=['subscribed', 'description'])
        for user in game['subscribed']['users']:
            notifications.add(user['user_id'], 'Игра "{}" была отредактирована.<br>Проверьте изменения!'.format(
                '<a href="/games?game_id={}">#{} | {}</a>'.format(
                    game_id,
                    game_id,
                    game['description'])
            ), 1)
        raise bottle.redirect('/games?game_id={}'.format(game_id))

    def post(self):
        if not pages.auth_dispatcher.organizer():
            return pages.PageBuilder('text', message='Недостаточно плав',
                                     description='Вы не можете просматривать эту страницу')
        if 'submit_add' in bottle.request.forms:
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
            _sport_types = sport_types.get(0, dbconnection=db)
            _game_types = game_types.get(0, dbconnection=db)
            _cities = cities.get(0, dbconnection=db)
            _courts = courts.get(0, fields=['court_id', 'city_id', 'title'], dbconnection=db)
            return pages.PageBuilder('editgame', game=game, sports=_sport_types, game_types=_game_types, cities=_cities,
                                     courts=_courts)

    def get_add(self):
        with modules.dbutils.dbopen() as db:
            _sports = sport_types.get(0, dbconnection=db)
            _game_types = game_types.get(0, dbconnection=db)
            _cities = cities.get(0, dbconnection=db)
            _courts = courts.get(0, fields=['court_id', 'city_id', 'title'], dbconnection=db)
            return pages.PageBuilder("addgame", sports=_sports, game_types=_game_types, cities=_cities, courts=_courts)

    def get_game_id(self):
        with modules.dbutils.dbopen() as db:
            game_id = int(bottle.request.query.get('game_id'))
            game = games.get_by_id(game_id, detalized=True, dbconnection=db)
            if len(game) == 0:
                return bottle.HTTPError(404)
            if pages.auth_dispatcher.loggedin() \
                    and pages.auth_dispatcher.getuserid() in {user['user_id'] for user in game['subscribed']['users']}:
                game['is_subscribed'] = True
            else:
                game['is_subscribed'] = False
            return pages.PageBuilder('game', game=game, standalone=True)

    def get_page(self, page_n):
        with modules.dbutils.dbopen() as db:
            count = int(db.execute("SELECT COUNT(game_id) FROM games")[0][0])
            total_pages = count // GAMES_PER_PAGE + 1
            if page_n > total_pages:
                raise bottle.HTTPError(404)
            allgames = games.get_recent(count=slice(*modules.pager(page_n, count=GAMES_PER_PAGE)), detalized=True,
                                        dbconnection=db)
            sports = sport_types.get(0, dbconnection=db)
            for game in allgames:
                if pages.auth_dispatcher.loggedin() \
                        and pages.auth_dispatcher.getuserid() in {user['user_id'] for user in
                                                                  game['subscribed']['users']}:
                    game['is_subscribed'] = True
                else:
                    game['is_subscribed'] = False
            page = pages.PageBuilder('games', games=allgames, sports=sports)
            if page_n < total_pages:
                page.add_param("nextpage", page_n + 1)
            return page

    def get(self):
        if 'delete' in bottle.request.query:
            if not pages.auth_dispatcher.organizer():
                return pages.PageBuilder('text', message='Недостаточно плав',
                                         description='Вы не можете просматривать эту страницу')
            games.delete(bottle.request.query.get('delete'))
            return bottle.redirect('/games')
        if 'add' in bottle.request.query:
            if pages.auth_dispatcher.organizer():
                return self.get_add()
            else:
                return pages.PageBuilder('text', message='Недостаточно плав',
                                         description='Вы не можете просматривать эту страницу')
        if 'edit' in bottle.request.query:
            if pages.auth_dispatcher.organizer():
                return self.get_edit()
            else:
                return pages.PageBuilder('text', message='Недостаточно плав',
                                         description='Вы не можете просматривать эту страницу')
        if 'game_id' in bottle.request.query:
            return self.get_game_id()
        if 'page' in bottle.request.query:
            return self.get_page(int(bottle.request.query.get('page')))
        return self.get_page(1)

    get.route = '/games'
    post.route = get.route