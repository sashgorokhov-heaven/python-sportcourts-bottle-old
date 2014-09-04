from modules import dbutils
from models import autodb, splitstrlist
from modules.utils import beautifuldate, beautifultime


@autodb
def add(user_id:int, text:str, level:int=0, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "INSERT INTO notifications (user_id, text, level) VALUES ({}, '{}', {})".format(
            user_id, text, level))


@autodb
def get_count(user_id:int, all:bool=False, dbconnection:dbutils.DBConnection=None) -> int:
    return int(dbconnection.execute("SELECT COUNT(*) FROM notifications WHERE user_id={}{}".format(
        user_id, ' AND `read`=0' if not all else ''))[0][0])


@autodb
def get(user_id:int, all:bool=False, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM notifications WHERE user_id={}{} ORDER BY DATETIME DESC{}".format(
        user_id, ' AND `read`=0' if not all else '', ' LIMIT 20' if all else ''),
                         dbutils.dbfields['notifications'])
    for i in dbconnection.last():
        dbutils.strdates(i)
        i['datetime'] = '{} {}'.format(beautifuldate(i['datetime']), beautifultime(i['datetime']))
    return dbconnection.last()


@autodb
def read(notification_id, dbconnection:dbutils.DBConnection=None):
    if isinstance(notification_id, str) and len(notification_id.split(',')) > 0:
        notification_id = splitstrlist(notification_id)
        if len(notification_id) == 1:
            notification_id = notification_id[0]

    if isinstance(notification_id, int) and notification_id > 0:
        dbconnection.execute(
            "UPDATE notifications SET `read`=1 WHERE `read`=0 AND notification_id={}".format(notification_id))
    elif isinstance(notification_id, list):
        dbconnection.execute("UPDATE notifications SET `read`=1 WHERE `read`=0 AND notification_id IN (" + ','.join(
            map(str, notification_id)) + ")")
    elif notification_id < 0:
        user_id = abs(notification_id)
        dbconnection.execute("UPDATE notifications SET `read`=1 WHERE `read`=0 AND user_id={}".format(user_id))


@autodb
def delete(notification_id, dbconnection:dbutils.DBConnection=None):
    if isinstance(notification_id, str) and len(notification_id.split(',')) > 0:
        notification_id = splitstrlist(notification_id)
        if len(notification_id) == 1:
            notification_id = notification_id[0]

    if isinstance(notification_id, int) and notification_id > 0:
        dbconnection.execute(
            "DELETE FROM notifications WHERE `read`=1 AND notification_id={}".format(notification_id))
    elif isinstance(notification_id, list):
        dbconnection.execute("DELETE FROM notifications WHERE `read`=1 AND notification_id IN (" + ','.join(
            map(str, notification_id)) + ")")
    elif notification_id < 0:
        user_id = abs(notification_id)
        dbconnection.execute("DELETE FROM notifications WHERE `read`=1 AND user_id={}".format(user_id))