import datetime

from modules import dbutils
from modules.utils import beautifuldate, beautifultime
from models import cities, autodb, splitstrlist, settings, ampluas

ADMIN = 0
ORGANIZER = 1
RESPONSIBLE = 2
COMMON = 3
JUDGE = 4


@autodb
def get(user_id, userlevel:int=-1, detalized:bool=False, count:slice=slice(0, 20),
        fields:list=dbutils.dbfields['users'],
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

    if userlevel >= 0 or isinstance(userlevel, set):
        sql += (' WHERE ' if user_id == 0 else ' AND ') + \
               ("LOCATE('|{}|', userlevel)".format(userlevel) if isinstance(userlevel, int) else ' AND '.join(
                   map(lambda x: "LOCATE('|{}|', userlevel)".format(x), userlevel)))

    if user_id == 0:
        sql += " LIMIT {}, {}".format(count.start if count.start else 0, count.stop)

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

        if 'userlevel' in user:
            user['userlevel'] = set(map(int, user['userlevel'].split('|')[1:-1]))

        if 'ampluas' in user:
            user['ampluas'] = ampluas.parse(user['ampluas'], detalized, dbconnection=dbconnection)

        if 'settings' in user and detalized:
            user['settings'] = settings.SettingsClass(user['settings'])

    if isinstance(user_id, int) and user_id != 0:
        return users[0]
    elif isinstance(user_id, list) or user_id == 0:
        return users


@autodb
def add_friend(user_id:int, friend_id:int, dbconnection:dbutils.DBConnection=None):
    if are_friends(user_id, friend_id, dbconnection=dbconnection):
        raise ValueError("User <{}> already have friend <{}>".format(user_id, friend_id))
    dbconnection.execute("INSERT INTO friends (user_id1, user_id2) VALUES ({},{})".format(user_id, friend_id))


@autodb
def remove_friend(user_id:int, friend_id:int, dbconnection:dbutils.DBConnection=None):
    if not are_friends(user_id, friend_id, dbconnection=dbconnection):
        raise ValueError("User <{}> do not have friend <{}>".format(user_id, friend_id))
    dbconnection.execute("DELETE FROM friends WHERE user_id1={} AND user_id2={}".format(user_id, friend_id))


@autodb
def are_friends(user_id_1:int, user_id_2:int, dbconnection:dbutils.DBConnection=None) -> bool:
    dbconnection.execute("SELECT * FROM friends WHERE user_id1={} AND user_id2={}".format(user_id_1, user_id_2))
    return len(dbconnection.last()) != 0


@autodb
def get_friends(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    friends = dbconnection.execute("SELECT user_id2 FROM friends WHERE user_id1={}".format(user_id))
    if len(friends)==0: return list()
    return get(list(map(lambda x: x[0], friends)), count=slice(0, len(friends)), detalized=True, dbconnection=dbconnection)
