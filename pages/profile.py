import bottle

import pages
import dbutils
from models import users, cities, images, games, ampluas


class Profile(pages.Page):
    def get_user_id(self):
        with dbutils.dbopen() as db:
            user_id = int(bottle.request.query.user_id)
            user = users.get(user_id, dbconnection=db)
            if len(user) == 0:
                raise bottle.HTTPError(404)
            page = pages.PageBuilder('profile', user=user,
                                     myfriend=users.are_friends(
                                         pages.auth.current().user_id(),
                                         user_id, dbconnection=db))
            page.add_param('user_games',
                           games.get_by_id(games.get_user_played_games(user_id, dbconnection=db), dbconnection=db))
            page.add_param('responsible_games',
                           games.get_by_id(games.get_responsible_games(user_id, dbconnection=db), dbconnection=db))
            page.add_param('organizer_games', games.get_all(dbconnection=db))
            return page

    def get_edit(self):
        with dbutils.dbopen() as db:
            _cities = cities.get(0, dbconnection=db)
            user = users.get(pages.auth.current().user_id(), dbconnection=db)
            _ampluas = ampluas.get(0, dbconnection=db)
            _ampluas = {
                sport_type_title: list(filter(lambda x: x.sport_type(True).title() == sport_type_title, _ampluas)) for
                sport_type_title in {i.sport_type(True).title() for i in _ampluas}}
            return pages.PageBuilder('editprofile', user=user, cities=_cities, ampluas=_ampluas,
                                     haveavatar=images.have_avatar(pages.auth.current().user_id()))

    def get(self):
        if 'user_id' in bottle.request.query:
            if int(bottle.request.query.get('user_id')) == pages.auth.current().user_id():
                raise bottle.redirect('/profile')
            return self.get_user_id()
        elif 'edit' in bottle.request.query and pages.auth.loggedin():
            return self.get_edit()
        elif 'addfriend' in bottle.request.query and pages.auth.loggedin():
            try:
                users.add_friend(pages.auth.current().user_id(), int(bottle.request.query.get('addfriend')))
            except ValueError:
                pass
            return ''
        elif 'removefriend' in bottle.request.query and pages.auth.loggedin():
            try:
                users.remove_friend(pages.auth.current().user_id(), int(bottle.request.query.get('removefriend')))
            except ValueError:
                pass
            return ''
        elif pages.auth.loggedin():
            with dbutils.dbopen() as db:
                user_id = pages.auth.current().user_id()
                user = users.get(user_id, dbconnection=db)
                page = pages.PageBuilder('profile', user=user)
                page.add_param('user_games',
                               games.get_by_id(games.get_user_played_games(user_id, dbconnection=db), dbconnection=db))
                page.add_param('responsible_games',
                               games.get_by_id(games.get_responsible_games(user_id, dbconnection=db), dbconnection=db))
                page.add_param('organizer_games',
                               games.get_by_id(games.get_organizer_games(user_id, dbconnection=db), dbconnection=db))
                return page
        return pages.templates.permission_denied(
            '<p><a class="btn btn-main btn-lg btn-success" href="/registration" role="button">Зарегестрируйтесь</a></p>',
            'Чтобы иметь свой профиль, с блекджеком и аватаркой.')

    def post(self):
        if not pages.auth.loggedin():
            return pages.templates.permission_denied()
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}

        city_title = params['city']
        params.pop('city')

        if 'ampluas[]' in params:
            params.pop('ampluas[]')
            params['ampluas'] = bottle.request.forms.getall('ampluas[]')
            params['ampluas'] = '|' + '|'.join(params['ampluas']) + '|'
        else:
            params['ampluas'] = ''

        if 'avatar' in params:
            if isinstance(params['avatar'], str):
                images.delete_avatar(pages.auth.current().user_id())
            params.pop('avatar')
        elif 'avatar' in bottle.request.files:
            images.save_avatar(pages.auth.current().user_id(), bottle.request.files.get('avatar'))

        with dbutils.dbopen() as db:
            db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
            if len(db.last()) > 0:
                params['city_id'] = db.last()[0][0]
            else:
                params['city_id'] = 1
            sql = "UPDATE users SET {} WHERE user_id={}".format(
                ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
                pages.auth.current().user_id())
            db.execute(sql)
            raise bottle.redirect('/profile')

    get.route = '/profile'
    post.route = get.route