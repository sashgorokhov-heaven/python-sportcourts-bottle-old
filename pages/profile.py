import os

from PIL import Image
import bottle

import pages
import modules
import modules.dbutils


class Profile(pages.Page):
    path = ['profile']

    def execute(self, method:str):
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data
        if method == 'POST':
            data = self.post()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    @pages.setlogin
    def get(self):
        if 'user_id' in bottle.request.query:
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(bottle.request.query.user_id)
                if len(user) == 0:
                    raise bottle.HTTPError(404)
                user = user[0]
                modules.dbutils.strdates(user)
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('profile', user=user)
        elif 'edit' in bottle.request.query and pages.loggedin():
            with modules.dbutils.dbopen() as db:
                cities = db.execute("SELECT city_id, title FROM cities", ['city_id', 'title'])
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                modules.dbutils.strdates(user)
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('editprofile', user=user, cities=cities)
        elif pages.loggedin():
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                modules.dbutils.strdates(user)
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('profile', user=user)
        raise bottle.HTTPError(404)

    @pages.setlogin
    def post(self):
        if not pages.loggedin():
            raise bottle.HTTPError(404)
        params = {i: bottle.request.forms[i] for i in bottle.request.forms}
        params.pop("submit_profile")
        params.pop("confirm_passwd")
        params.pop("city")
        params['city_id'] = 1

        params['first_name'] = bottle.request.forms.getunicode('first_name')
        params['middle_name'] = bottle.request.forms.getunicode('middle_name')
        params['last_name'] = bottle.request.forms.getunicode('last_name')

        if 'avatar' in params:
            params.pop('avatar')

        if 'avatar' in bottle.request.files:
            filename = str(pages.getuserid()) + '.jpg'
            dirname = '/bsp/data/avatars'
            fullname = os.path.join(dirname, filename)
            if os.path.exists(fullname):
                os.remove(fullname)
            bottle.request.files.get('avatar').save(fullname)
            Image.open(fullname).crop().resize((200, 200)).save(fullname)
            print(fullname)

        with modules.dbutils.dbopen() as db:
            sql = "UPDATE users SET {} WHERE user_id={}".format(
                ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
                pages.getuserid())
            db.execute(sql)
            bottle.redirect('/profile')
