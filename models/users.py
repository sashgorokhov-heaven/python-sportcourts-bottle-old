import datetime

from modules import dbutils
from modules.utils import beautifuldate, beautifultime
from models import cities, autodb, splitstrlist, settings


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
        if len(user_id) == 0: return list()
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

        if 'friends' in user:
            friends = list(map(int, user['friends'].split('|')[1:-1]))
            user['friends'] = {'count': len(friends), 'users': friends}
            if detalized:
                user['friends']['users'] = get(user['friends']['users'], fields=['user_id', 'first_name', 'last_name'],
                                               dbconnection=dbconnection)

        if 'settings' in user and detalized:
            user['settings'] = settings.SettingsClass(user['settings'])

    if isinstance(user_id, int) and user_id != 0:
        return users[0]
    elif isinstance(user_id, list) or user_id == 0:
        return users


@autodb
def add_friend(user_id:int, friend_id:int, dbconnection:dbutils.DBConnection=None):
    friends = dbconnection.execute("SELECT friends FROM users WHERE user_id='{}'".format(user_id))[0][0]
    friends = list(map(int, friends.split('|')[1:-1]))
    if friend_id in set(friends):
        raise ValueError("User <{}> already have friend <{}>".format(user_id, friend_id))
    friends.append(friend_id)
    if len(friends) > 0:
        friends = '|' + '|'.join(map(str, friends)) + '|'
    else:
        friends = ''
    dbconnection.execute("UPDATE users SET friends='{}' WHERE user_id={}".format(friends, user_id))


@autodb
def are_friends(user_id_1:int, user_id_2:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "SELECT user_id FROM users WHERE user_id='{}' AND LOCATE('|{}|', friends)".format(user_id_1, user_id_2))
    return len(dbconnection.last()) != 0