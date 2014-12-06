import datetime
import pages
import dbutils
import json
from modules import logging


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            return dump({'error':e.__class__.__name__, 'description':(e.args[-1] if len(e.args)>0 else '')})
    return wrapper


def strdatetime(d:dict) -> dict:
    for key in d:
        if isinstance(d[key], (datetime.datetime, datetime.date, datetime.time)):
            d[key] = str(d[key])
    return d


@pages.get('/api/users/get')
#@pages.only_ajax
@pages.only_admins
@handle_error
def users_get():
    with dbutils.dbopen() as db:
        users = db.execute("SELECT * FROM users", dbutils.dbfields['users'])
        list(map(strdatetime, users))
        return dump({'count':len(users), 'users':users})


@pages.get('/api/courts/get')
#@pages.only_ajax
@pages.only_admins
@handle_error
def courts_get():
    with dbutils.dbopen() as db:
        courts = db.execute("SELECT * FROM courts", dbutils.dbfields['courts'])
        list(map(strdatetime, courts))
        return dump({'count':len(courts), 'courts':courts})