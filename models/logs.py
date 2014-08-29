from models import autodb
from modules import dbutils


@autodb
def add(user_id:int, text:str, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("INSERT INTO logs (user_id, text) VALUES ({}, '{}')".format(user_id, text))