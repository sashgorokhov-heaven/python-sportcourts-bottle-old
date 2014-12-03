import dbutils
from models import autodb
import cacher


@cacher.create_table_name('banned', 'user_id', 600, cacher.KeyCache)
@autodb
def banned(user_id:int, dbconnection:dbutils.DBConnection=None) -> bool:
    dbconnection.execute("SELECT user_id FROM banned WHERE user_id={}".format(user_id))
    return len(dbconnection.last()) != 0


@autodb
def get_ban_message(user_id:int, dbconnection:dbutils.DBConnection=None) -> str:
    if not banned(user_id, dbconnection=dbconnection):
        raise ValueError("User <{}> not banned".format(user_id))
    return dbconnection.execute("SELECT reason FROM banned WHERE user_id={}".format(user_id))[0][0]


@autodb
def ban(user_id:int, reason:str, dbconnection:dbutils.DBConnection=None):
    if banned(user_id, dbconnection=dbconnection):
        raise ValueError("User already banned")
    dbconnection.execute("INSERT INTO banned (user_id, reason) VALUES (user_id, '{}')".format(user_id, reason))
    cacher.drop_by_table_name('banned', 'user_id', user_id)