import bottle

import pages
import modules
import modules.dbutils


class Profile(pages.Page):
    path = ['profile']

    def execute(self, method:str):
        data = self.get()
        if isinstance(data, pages.Template):
            return data.template()
        return data

    @pages.setlogin
    @pages.handleerrors
    def get(self):
        if 'user_id' in bottle.request.query:
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(bottle.request.query.user_id)
                if len(user) == 0:
                    raise bottle.HTTPError(404)
                return pages.Template('profile', user=user[0])
        elif pages.loggedin():
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                return pages.Template('profile', user=user)
        raise bottle.HTTPError(404)