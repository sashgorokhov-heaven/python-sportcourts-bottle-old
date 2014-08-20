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
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                modules.dbutils.strdates(user)
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('editprofile', user=user)
        elif pages.loggedin():
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                modules.dbutils.strdates(user)
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('profile', user=user)
        raise bottle.HTTPError(404)