from models import autodb, splitstrlist
from modules import dbutils


@autodb
def get(type_id, fields:list=dbutils.dbfields['game_types'], dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['game_types'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(type_id, str) and len(type_id.split(',')) > 0:
        type_id = splitstrlist(type_id)

    if isinstance(type_id, int) and type_id != 0:
        dbconnection.execute("SELECT " + select + " FROM game_types WHERE type_id='{}'".format(type_id), orderedfields)
    elif isinstance(type_id, list):
        dbconnection.execute(
            "SELECT " + select + " FROM game_types WHERE type_id IN (" + ','.join(map(str, type_id)) + ")",
            orderedfields)
    elif type_id == 0:
        dbconnection.execute("SELECT " + select + " FROM game_types", orderedfields)

    if len(dbconnection.last()) == 0:
        return list()
    game_types = dbconnection.last()

    if isinstance(type_id, int) and type_id != 0:
        return game_types[0]
    elif isinstance(type_id, list) or type_id == 0:
        return game_types


@autodb
def get_by_sport(sport_type, fields:list=dbutils.dbfields['game_types'],
                 dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['game_types'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(sport_type, str) and len(sport_type.split(',')) > 0:
        sport_type = splitstrlist(sport_type)
        if len(sport_type) == 1:
            sport_type = sport_type[0]

    if isinstance(sport_type, int) and sport_type != 0:
        dbconnection.execute("SELECT " + select + " FROM game_types WHERE sport_type='{}'".format(sport_type),
                             orderedfields)
    elif isinstance(sport_type, list):
        dbconnection.execute(
            "SELECT " + select + " FROM game_types WHERE sport_type IN (" + ','.join(map(str, sport_type)) + ")",
            orderedfields)
    elif sport_type == 0:
        dbconnection.execute("SELECT " + select + " FROM game_types", orderedfields)

    if len(dbconnection.last()) == 0:
        return list()
    game_types = dbconnection.last()

    return game_types