from modules import dbutils
from models import cities, sport_types, autodb, splitstrlist


@autodb
def get(court_id, city_id:int=1, detalized:bool=False, fields:list=dbutils.dbfields['courts'],
        dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['courts'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(court_id, str) and len(court_id.split(',')) > 0:
        court_id = splitstrlist(court_id)
        if len(court_id) == 1:
            court_id = court_id[0]

    if isinstance(court_id, int) and court_id != 0:
        dbconnection.execute(
            "SELECT " + select + " FROM courts WHERE court_id={} AND city_id={}".format(court_id, city_id),
            orderedfields)
    elif isinstance(court_id, list):
        dbconnection.execute(
            "SELECT " + select + " FROM courts WHERE court_id IN (" + ','.join(
                map(str, court_id)) + ") AND city_id={}".format(city_id), orderedfields)
    elif court_id == 0:
        dbconnection.execute("SELECT " + select + " FROM courts WHERE city_id={}".format(city_id), orderedfields)

    if len(dbconnection.last()) == 0:
        return list()
    courts = dbconnection.last()

    for court in courts:
        if 'sport_types' in court and detalized:
            court['sport_types'] = sport_types.get(court['sport_types'], dbconnection=dbconnection)
        if 'city_id' in court and detalized:
            court['city'] = cities.get(court['city_id'], dbconnection=dbconnection)
            court.pop('city_id')

    if isinstance(court_id, int) and court_id != 0:
        return courts[0]
    elif isinstance(court_id, list) or court_id == 0:
        return courts
