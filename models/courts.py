import dbutils
from objects import Court
from models import autodb, splitstrlist
import cacher


@cacher.create_table_name('courts', 'court_id', 600, cacher.SimpleCache, 'court_id')
@autodb
def get(court_id, city_id:int=1, dbconnection:dbutils.DBConnection=None) -> Court:
    if isinstance(court_id, str) and len(court_id.split(',')) > 0:
        court_id = splitstrlist(court_id)
        if len(court_id) == 1:
            court_id = court_id[0]

    if isinstance(court_id, list) and len(court_id) == 0: return list()

    if isinstance(court_id, int) and court_id != 0:
        dbconnection.execute(
            "SELECT * FROM courts WHERE court_id={} AND city_id={}".format(court_id, city_id),
            dbutils.dbfields['courts'])
    elif isinstance(court_id, list):
        dbconnection.execute(
            "SELECT * FROM courts WHERE court_id IN (" + ','.join(
                map(str, court_id)) + ") AND city_id={}".format(city_id), dbutils.dbfields['courts'])
    elif court_id == 0:
        dbconnection.execute("SELECT * FROM courts WHERE city_id={}".format(city_id), dbutils.dbfields['courts'])

    if len(dbconnection.last()) == 0: return list()

    courts = dbconnection.last()
    courts = list(map(lambda x: Court(x, dbconnection=dbconnection), courts))

    if isinstance(court_id, int) and court_id != 0:
        return courts[0]
    elif isinstance(court_id, list) or court_id == 0:
        return courts
