import dbutils
from models import autodb, splitstrlist, Cache
from objects import GameType


_cache = Cache(600, 'type_id')


@_cache
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