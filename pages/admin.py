import bottle
import pages
import dbutils

class Admin(pages.Page):
    def get(self, **kwargs):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            users = db.execute("SELECT user_id, first_name, last_name, email, phone  FROM users")
            users = list(map(lambda x: [x[0], x[1]+' '+x[2], x[3], x[4]], users))
            return pages.PageBuilder('admin', users=users)

    get.route = '/admin'