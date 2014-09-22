import bottle

import pages
import modules
import modules.dbutils
from models import users, cities, activation, images, usergames


class Profile(pages.Page):
    def get_user_id(self):
        with modules.dbutils.dbopen() as db:
            user_id = int(bottle.request.query.user_id)
            user = users.get(user_id, detalized=True, dbconnection=db)
            if len(user) == 0:
                raise bottle.HTTPError(404)
            user['gameinfo'] = usergames.get_game_stats(user_id, dbconnection=db)
            return pages.PageBuilder('profile', user=user)

    def get_edit(self):
        with modules.dbutils.dbopen() as db:
            _cities = cities.get(0, dbconnection=db)
            user = users.get(pages.auth_dispatcher.getuserid(), detalized=True, dbconnection=db)
            return pages.PageBuilder('editprofile', user=user, cities=_cities,
                                     haveavatar=images.have_avatar(pages.auth_dispatcher.getuserid()))

    def get(self):
        if 'user_id' in bottle.request.query:
            if int(bottle.request.query.get('user_id')) == pages.auth_dispatcher.getuserid():
                raise bottle.redirect('/profile')
            return self.get_user_id()
        elif 'edit' in bottle.request.query and pages.auth_dispatcher.loggedin():
            return self.get_edit()
        elif 'addfriend' in bottle.request.query and pages.auth_dispatcher.loggedin():
            try:
                users.add_friend(pages.auth_dispatcher.getuserid(), int(bottle.request.query.get('addfriend')))
            except ValueError:
                pass
            return ''
        elif 'removefriend' in bottle.request.query and pages.auth_dispatcher.loggedin():
            try:
                users.remove_friend(pages.auth_dispatcher.getuserid(), int(bottle.request.query.get('removefriend')))
            except ValueError:
                pass
            return ''
        elif pages.auth_dispatcher.loggedin():
            with modules.dbutils.dbopen() as db:
                user_id = pages.auth_dispatcher.getuserid()
                user = users.get(user_id, detalized=True, dbconnection=db)
                user['gameinfo'] = usergames.get_game_stats(user_id, dbconnection=db)
                activated = activation.activated(user_id, dbconnection=db)
                return pages.PageBuilder('profile', user=user, activated=activated)
        return pages.templates.permission_denied("Ошибка доступа",
                                                 "Зарегестрируйтесь, чтобы иметь свой профиль, с блекджеком и аватаркой.")

    def post(self):
        if not pages.auth_dispatcher.loggedin():
            return pages.templates.permission_denied()
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}

        city_title = params['city']
        params.pop('city')

        if 'avatar' in params:
            params.pop('avatar')

        if 'avatar' in bottle.request.files:
            images.save_avatar(pages.auth_dispatcher.getuserid(), bottle.request.files.get('avatar'))
        else:
            images.delete_avatar(pages.auth_dispatcher.getuserid())

        with modules.dbutils.dbopen() as db:
            db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
            if len(db.last()) > 0:
                params['city_id'] = db.last()[0][0]
            else:
                params['city_id'] = 1
            sql = "UPDATE users SET {} WHERE user_id={}".format(
                ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
                pages.auth_dispatcher.getuserid())
            db.execute(sql)
            raise bottle.redirect('/profile')

    get.route = '/profile'
    post.route = get.route