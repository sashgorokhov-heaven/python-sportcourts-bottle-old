import dbutils
from objects import User

from models import autodb, splitstrlist

ADMIN = 0
ORGANIZER = 1
RESPONSIBLE = 2
COMMON = 3
JUDGE = 4


@autodb
def get(user_id, userlevel:int=-1, activated:int=0, count:slice=slice(0, 20), dbconnection:dbutils.DBConnection=None) -> User:
    if isinstance(user_id, str) and len(user_id.split(',')) > 0:
        user_id = splitstrlist(user_id)
        if len(user_id) == 1:
            user_id = user_id[0]

    if isinstance(user_id, list) and len(user_id) == 0: return list()

    sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)

    if isinstance(user_id, int) and user_id != 0:
        sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)
    elif isinstance(user_id, list):
        sql = "SELECT * FROM users WHERE user_id IN (" + ','.join(map(str, user_id)) + ")"
    elif user_id == 0:
        sql = "SELECT * FROM users"

    if userlevel >= 0 or isinstance(userlevel, set):
        if user_id==0:
            sql += ' WHERE '
        else:
            sql += ' AND '
        if isinstance(userlevel, int):
            sql += " LOCATE('|{}|', userlevel) ".format(userlevel)
        else:
            ' AND '.join(map(lambda x: "LOCATE('|{}|', userlevel)".format(x), userlevel))

    if activated>0:
        sql += ' {} activated=1 '.format('WHERE' if user_id==0 else 'AND')
    elif activated<0:
        sql += ' {} activated=0 '.format('WHERE' if user_id==0 else 'AND')

    if user_id == 0:
        sql += " LIMIT {}, {}".format(count.start if count.start else 0, count.stop)

    dbconnection.execute(sql, dbutils.dbfields['users'])

    if len(dbconnection.last()) == 0: return list()

    users = dbconnection.last()
    users = list(map(lambda x: User(x, dbconnection=dbconnection), users))

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
    return list(map(lambda x: x[0], friends)) if len(friends) > 0 else list()


@autodb
def search(query:str, dbconnection:dbutils.DBConnection=None) -> list:
    query = list(map(lambda x: '%' + x + '%', query.split(' ')))
    sql = "SELECT user_id FROM users WHERE "
    if len(query) == 1:
        sql += "first_name LIKE '{first}' OR last_name LIKE '{first}'".format(first=query[0])
    else:
        sql += ("first_name LIKE '{first}' AND last_name LIKE '{last}'"
                " OR "
                "first_name LIKE '{last}' AND last_name LIKE '{first}'").format(first=query[0], last=query[1])
    users = dbconnection.execute(sql)
    return list(map(lambda x: x[0], users)) if len(users) > 0 else list()