from models import autodb
from modules import dbutils


@autodb
def get(sport_id, fields:list=dbutils.dbfields['sport_types'], dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['sport_types'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(sport_id, str) and len(sport_id.split(',')) > 0:
        sport_id = list(filter(lambda x: x != '', map(lambda x: x.strip(), sport_id.split(','))))
        if len(sport_id) == 1:
            sport_id = sport_id[0]

    if isinstance(sport_id, int) and sport_id != 0:
        dbconnection.execute("SELECT " + select + " FROM sport_types WHERE sport_id='{}'".format(sport_id),
                             orderedfields)
    elif isinstance(sport_id, list):
        dbconnection.execute(
            "SELECT " + select + " FROM sport_types WHERE sport_id IN (" + ','.join(map(str, sport_id)) + ")",
            orderedfields)
    elif sport_id == 0:
        dbconnection.execute("SELECT " + select + " FROM sport_types", orderedfields)

    if len(dbconnection.last()) == 0:
        return list()
    sport_types = dbconnection.last()

    if isinstance(sport_id, int) and sport_id != 0:
        return sport_types[0]
    elif isinstance(sport_id, list) or sport_id == 0:
        return sport_types