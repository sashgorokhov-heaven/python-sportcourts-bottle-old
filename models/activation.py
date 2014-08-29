from models import autodb
from modules import dbutils


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