import datetime
import json

from modules import dbutils
from modules.utils import beautifuldate, beautifultime
from models import cities, autodb, splitstrlist, settings

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

        if 'friends' in user:
            friends = list(map(int, user['friends'].split('|')[1:-1]))
            user['friends'] = {'count': len(friends), 'users': friends}
            if detalized:
                user['friends']['users'] = get(user['friends']['users'], fields=['user_id', 'first_name', 'last_name'],
                                               dbconnection=dbconnection)

        if 'settings' in user and detalized:
            user['settings'] = settings.SettingsClass(user['settings'])

        if 'gameinfo' in user and detalized:
            user['gameinfo'] = _GameInfo(user['gameinfo'])

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
def remove_friend(user_id:int, friend_id:int, dbconnection:dbutils.DBConnection=None):
    friends = dbconnection.execute("SELECT friends FROM users WHERE user_id='{}'".format(user_id))[0][0]
    friends = list(map(int, friends.split('|')[1:-1]))
    if friend_id not in set(friends):
        raise ValueError("User <{}> do not have friend <{}>".format(user_id, friend_id))
    friends.remove(friend_id)
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


class _GameInfo:
    def __init__(self, gameinfo:str):
        self._gameinfo = json.loads(gameinfo)

    def set(self, sport_type:str, duration:int):
        if sport_type not in self._gameinfo['sport_types']:
            self._gameinfo['sport_types'][sport_type] = 0
        self._gameinfo['sport_types'][sport_type] += duration
        self._gameinfo['sport_types']['total'] += duration

    def get(self, sport_type:str, formatted:bool=False) -> int:
        if sport_type not in self._gameinfo['sport_types']:
            return 0 if not formatted else '0', 'минут'
        return self._gameinfo['sport_types'][sport_type] if not formatted else self._format(
            self._gameinfo['sport_types'][sport_type])

    def total(self, formatted:bool=False) -> int:
        return self._gameinfo['sport_types']['total'] if not formatted else self._format(
            self._gameinfo['sport_types']['total'])

    def format(self) -> str:
        return json.dumps(self._gameinfo)

    def _format(self, duration:int) -> tuple:
        postfix = 'минут'
        prefix = int(str(duration)[-1])
        if prefix == 0 or 5 <= prefix <= 9:
            postfix = 'минут'
        elif prefix == 1:
            postfix = 'минута'
        elif 2 <= prefix <= 4:
            postfix = 'минуты'
        if duration > 60:
            duration = round(duration / 60)
            prefix = int(str(duration)[-1])
            if prefix == 0 or 5 <= prefix <= 9:
                postfix = 'часов'
            elif prefix == 1:
                postfix = 'час'
            elif 2 <= prefix <= 4:
                postfix = 'часа'
            if duration > 24:
                duration = round(duration / 24)
                prefix = int(str(duration)[-1])
                if prefix == 0 or 5 <= prefix <= 9:
                    postfix = 'дней'
                elif prefix == 1:
                    postfix = 'день'
                elif 2 <= prefix <= 4:
                    postfix = 'дня'
        return str(duration), postfix

    def __iter__(self):
        d = self._gameinfo['sport_types']
        d.pop('total')
        return d.__iter__()


def update_gameinfo(user_id:int, gameinfo:_GameInfo, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("UPDATE users SET gameinfo='{}' WHERE user_id={}".format(gameinfo.format(), user_id))
