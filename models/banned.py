from models import autodb
from modules import dbutils


@autodb
def banned(user_id:int, dbconnection:dbutils.DBConnection=None) -> bool:
    dbconnection.execute("SELECT reason FROM banned WHERE user_id='{}'".format(user_id))
    if len(dbconnection.last()) == 0:
        return False
    return dbconnection.last()[0][0]


@autodb
def ban(user_id:int, reason:str, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("INSERT INTO banned (user_id, reason) VALUES ({}, '{}')".format(user_id, reason))