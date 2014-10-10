import dbutils
from models import autodb, splitstrlist, SimpleCache
from objects import City


_cache = SimpleCache(600, 'city_id')


@_cache
@autodb
def get(city_id, dbconnection:dbutils.DBConnection=None) -> City:
    if isinstance(city_id, str) and len(city_id.split(',')) > 0:
        city_id = splitstrlist(city_id)
        if len(city_id) == 1:
            city_id = city_id[0]

    if isinstance(city_id, list) and len(city_id)==0: return list()

    if isinstance(city_id, int) and city_id != 0:
        dbconnection.execute("SELECT * FROM cities WHERE city_id='{}'".format(city_id), dbutils.dbfields['cities'])
    elif isinstance(city_id, list):
        dbconnection.execute("SELECT * FROM cities WHERE city_id IN (" + ','.join(map(str, city_id)) + ")",
                             dbutils.dbfields['cities'])
    elif city_id == 0:
        dbconnection.execute("SELECT * FROM cities", dbutils.dbfields['cities'])

    if len(dbconnection.last()) == 0: return list()

    cities = dbconnection.last()
    cities = list(map(lambda x: City(x), cities))

    if isinstance(city_id, int) and city_id != 0:
        return cities[0]
    elif isinstance(city_id, list) or city_id == 0:
        return cities