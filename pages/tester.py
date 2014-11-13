import bottle
import pages
import dbutils
import datetime

class Tester(pages.Page):
    def get(self, **kwargs):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            db.execute("SELECT NOW();")
            return 'Database time: {}<br>Python time: {}'.format(db.last()[0][0], datetime.datetime.now())

    get.route = '/tester'