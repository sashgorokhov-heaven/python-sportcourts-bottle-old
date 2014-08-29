from models import autodb, splitstrlist
from modules import dbutils


@autodb
def get(city_id, fields:list=dbutils.dbfields['cities'], dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['cities'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(city_id, str) and len(city_id.split(',')) > 0:
        city_id = splitstrlist(city_id)
        if len(city_id) == 1:
            city_id = city_id[0]

    if isinstance(city_id, int) and city_id != 0:
        dbconnection.execute("SELECT " + select + " FROM cities WHERE city_id='{}'".format(city_id), orderedfields)
    elif isinstance(city_id, list):
        dbconnection.execute("SELECT " + select + " FROM cities WHERE city_id IN (" + ','.join(map(str, city_id)) + ")",
                             orderedfields)
    elif city_id == 0:
        dbconnection.execute("SELECT " + select + " FROM cities", orderedfields)

    if len(dbconnection.last()) == 0:
        return list()

    cities = dbconnection.last()

    if isinstance(city_id, int) and city_id != 0:
        return cities[0]
    elif isinstance(city_id, list) or city_id == 0:
        return cities