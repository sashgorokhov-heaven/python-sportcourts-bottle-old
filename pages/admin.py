import bottle
import json
import pages
import dbutils
from models import finances, logs

def get_finances(db:dbutils.DBConnection) -> dict:
    return {'fin':finances.Finances(0, db)}


def get_users(db:dbutils.DBConnection) -> dict:
    users = db.execute("SELECT user_id, first_name, last_name, email, phone  FROM users",
                       ['user_id', 'first_name', 'last_name', 'email', 'phone'])
    return {'users': json.dumps(users)}


def get_logs(db:dbutils.DBConnection) -> dict:
    return {'log':logs.Logs(db)}


class Admin(pages.Page):
    def get(self, **kwargs):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            respdict = get_users(db)
            respdict.update(get_finances(db))
            respdict.update(get_logs(db))
            return pages.PageBuilder('admin', **respdict)

    get.route = '/admin'