from models import autodb
from modules import dbutils
import modules


@autodb
def activated(user_id:int, dbconnection:dbutils.DBConnection=None) -> bool:
    dbconnection.execute("SELECT * FROM activation WHERE user_id='{}'".format(user_id))
    return len(dbconnection.last()) == 0


@autodb
def activate(user_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("UPDATE users SET activated=1 WHERE user_id={}".format(user_id))
    dbconnection.execute("DELETE FROM activation WHERE user_id={}".format(user_id))


@autodb
def get_userid_by_token(token:str, dbconnection:dbutils.DBConnection=None) -> int:
    dbconnection.execute("SELECT user_id FROM activation WHERE token='{}'".format(token))
    if len(dbconnection.last()) == 0:
        raise ValueError("User activated or not exist")
    return dbconnection.last()[0][0]


@autodb
def create(user_id:int, dbconnection:dbutils.DBConnection=None) -> str:
    token = modules.generate_token()
    dbconnection.execute("INSERT INTO activation (user_id, token) VALUES ({}, '{}')".format(user_id, token))
    return token


@autodb
def get_user_token(user_id:int, dbconnection:dbutils.DBConnection=None) -> str:
    dbconnection.execute("SELECT token FROM activation WHERE user_id={}".format(user_id))
    if len(dbconnection.last()) == 0:
        raise ValueError("User activated or not exist")
    return dbconnection.last()[0][0]