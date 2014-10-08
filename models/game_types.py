import dbutils
from models import autodb, splitstrlist
from objects import GameType


@autodb
def get(type_id, dbconnection:dbutils.DBConnection=None) -> GameType:
    if isinstance(type_id, str) and len(type_id.split(',')) > 0:
        type_id = splitstrlist(type_id)
        if len(type_id) == 1:
            type_id = type_id[0]

    if isinstance(type_id, list) and len(type_id)==0: return list()

    if isinstance(type_id, int) and type_id != 0:
        dbconnection.execute("SELECT * FROM game_types WHERE type_id='{}'".format(type_id), dbutils.dbfields['game_types'])
    elif isinstance(type_id, list):
        dbconnection.execute(
            "SELECT * FROM game_types WHERE type_id IN (" + ','.join(map(str, type_id)) + ")",
            dbutils.dbfields['game_types'])
    elif type_id == 0:
        dbconnection.execute("SELECT * FROM game_types", dbutils.dbfields['game_types'])

    if len(dbconnection.last()) == 0: return list()

    game_types = dbconnection.last()
    game_types = list(map(lambda x: GameType(x, dbconnection=dbconnection), game_types))

    if isinstance(type_id, int) and type_id != 0:
        return game_types[0]
    elif isinstance(type_id, list) or type_id == 0:
        return game_types


#@autodb
#def get_by_sport(sport_type, dbconnection:dbutils.DBConnection=None) -> list:
#    if isinstance(sport_type, str) and len(sport_type.split(',')) > 0:
#        sport_type = splitstrlist(sport_type)
#        if len(sport_type) == 1:
#            sport_type = sport_type[0]
#
#    if isinstance(sport_type, list) and len(sport_type)==0: return list()
#
#    if isinstance(sport_type, int) and sport_type != 0:
#        dbconnection.execute("SELECT * FROM game_types WHERE sport_type='{}'".format(sport_type),
#                             dbutils.dbfields['game_types'])
#    elif isinstance(sport_type, list):
#        dbconnection.execute(
#            "SELECT * FROM game_types WHERE sport_type IN (" + ','.join(map(str, sport_type)) + ")",
#            dbutils.dbfields['game_types'])
#    elif sport_type == 0:
#        dbconnection.execute("SELECT * FROM game_types", dbutils.dbfields['game_types'])
#
#    if len(dbconnection.last()) == 0: return list()
#
#    game_types = dbconnection.last()
#    game_types = list(map(lambda x: GameType(x, dbconnection=dbconnection), game_types))
#
#    if isinstance(sport_type, int) and sport_type != 0:
#        return game_types[0]
#    elif isinstance(sport_type, list) or sport_type == 0:
#        return game_types