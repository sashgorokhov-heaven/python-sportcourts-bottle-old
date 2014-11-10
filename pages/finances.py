import bottle
import dbutils
from models import finances
import pages

class Finances1(pages.Page):
    def get(self):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            if 'month' in bottle.request.query:
                month = int(bottle.request.query.get('month'))
            else:
                month = 0
            fin = finances.Finances(month, db)
            return pages.PageBuilder('finances', **fin.dict())

    get.route = '/admin/finances'