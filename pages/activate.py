import bottle

from modules import dbutils
import modules
import pages


class Activate(pages.Page):
    path = ['activate']

    def execute(self, method:str):
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    @pages.handleerrors("404")
    def get(self):
        token = bottle.request.query.get('token')
        with dbutils.dbopen() as db:
            db.execute("SELECT user_id FROM activation WHERE token='{}'".format(token))
            if len(db.last()) == 0:
                raise bottle.HTTPError(404)
            user_id = db.last()[0][0]
            db.execute("UPDATE users SET activated={} WHERE user_id={}".format(1, user_id))
            db.execute("DELETE FROM activation WHERE user_id={}".format(user_id))
            bottle.response.set_cookie('activated', 1, modules.config['secret'])
            raise bottle.redirect('/auth')