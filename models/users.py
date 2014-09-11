import datetime

from modules import dbutils
from modules.utils import beautifuldate, beautifultime
from models import cities, autodb, splitstrlist


@autodb
def get(user_id, userlevel:int=-1, detalized:bool=False, fields:list=dbutils.dbfields['users'],
        dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['users'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(user_id, str) and len(user_id.split(',')) > 0:
        user_id = splitstrlist(user_id)
        if len(user_id) == 1:
            user_id = user_id[0]
    if isinstance(user_id, int) and user_id != 0:
        sql = "SELECT " + select + " FROM users WHERE user_id='{}'".format(user_id)
    elif isinstance(user_id, list):
        sql = "SELECT " + select + " FROM users WHERE user_id IN (" + ','.join(map(str, user_id)) + ")"
    elif user_id == 0:
        sql = "SELECT " + select + " FROM users"

    if userlevel >= 0:
        sql += (' WHERE ' if user_id == 0 else ' AND ') + 'userlevel={}'.format(userlevel)

    dbconnection.execute(sql, orderedfields)

    if len(dbconnection.last()) == 0:
        return list()
    users = dbconnection.last()

    for user in users:
        dbutils.strdates(user)
        if 'bdate' in user:
            age = str(round((datetime.date.today() - datetime.date(
                *list(map(int, user['bdate'].split('-'))))).total_seconds() // 31556926))
            postfix = ''
            prefix = int(age[-1])
            if prefix == 0 or 5 <= prefix <= 9:
                postfix = 'лет'
            elif prefix == 1:
                postfix = 'год'
            elif 2 <= prefix <= 4:
                postfix = 'года'
            user['parsed_bdate'] = age + ' ' + postfix
        if 'lasttime' in user:
            date = user['lasttime'].split(' ')[0]
            timedelta = (datetime.date.today() - datetime.date(*map(int, date.split('-')))).days
            if timedelta == 0:
                date = 'сегодня'
            elif timedelta == 1:
                date = 'вчера'
            else:
                date = beautifuldate(user['lasttime'])
            user['lasttime'] = '{} в {}'.format(date, beautifultime(user['lasttime']))
        if detalized and 'city_id' in user:
            user['city'] = cities.get(user['city_id'], dbconnection=dbconnection)
            user.pop('city_id')

    if isinstance(user_id, int) and user_id != 0:
        return users[0]
    elif isinstance(user_id, list) or user_id == 0:
        return users