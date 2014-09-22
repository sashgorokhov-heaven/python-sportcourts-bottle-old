from models import autodb, games
from modules import dbutils


@autodb
def get(user_id:int, status:int=-1, detalized:bool=False, fields:list=dbutils.dbfields['games'],
        dbconnection:dbutils.DBConnection=None) -> list:  # list of dict
    usergames = dbconnection.execute("SELECT game_id, status FROM usergames WHERE user_id={}{}".format(user_id,
                                                                                                       '' if status < 0 else "AND status={}".format(
                                                                                                           status)),
                                     ['game_id', 'status'])
    if not detalized:
        return usergames
    game_ids = list(map(lambda x: x['game_id'], usergames))
    return games.get_by_id(game_ids, detalized=True, fields=fields, dbconnection=dbconnection)


@autodb
def set(user_id:int, game_id:int, status:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "INSERT INTO usergames (user_id, game_id, status) VALUES ({}, {}, {})".format(user_id, game_id, status))