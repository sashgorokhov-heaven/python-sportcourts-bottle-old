import dbutils
from models import autodb, splitstrlist
from objects import SportType


@autodb
def get(sport_id, dbconnection:dbutils.DBConnection=None) -> list:
    if isinstance(sport_id, str) and len(sport_id.split(',')) > 0:
        sport_id = splitstrlist(sport_id)
        if len(sport_id) == 1:
            sport_id = sport_id[0]

    if isinstance(sport_id, list) and len(sport_id)==0: return list()

    if isinstance(sport_id, int) and sport_id != 0:
        dbconnection.execute("SELECT * FROM sport_types WHERE sport_id='{}'".format(sport_id),
                             dbutils.dbfields['sport_types'])
    elif isinstance(sport_id, list):
        dbconnection.execute(
            "SELECT * FROM sport_types WHERE sport_id IN (" + ','.join(map(str, sport_id)) + ")",
            dbutils.dbfields['sport_types'])
    elif sport_id == 0:
        dbconnection.execute("SELECT * FROM sport_types", dbutils.dbfields['sport_types'])

    if len(dbconnection.last()) == 0: return list()

    sport_types = dbconnection.last()
    sport_types = list(map(lambda x: SportType(x), sport_types))

    if isinstance(sport_id, int) and sport_id != 0:
        return sport_types[0]
    elif isinstance(sport_id, list) or sport_id == 0:
        return sport_types