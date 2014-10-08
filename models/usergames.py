import dbutils
from models import autodb, games
from objects import Game
from modules.utils import format_duration


@autodb
def get(user_id:int, status:int=-1, dbconnection:dbutils.DBConnection=None) -> list:
    sql = "SELECT game_id, status FROM usergames WHERE user_id={}{}"
    usergames = dbconnection.execute(sql.format(user_id, '' if status < 0 else " AND status={}".format(status)),
                                     ['game_id', 'status'])
    if len(usergames)==0: return list()
    game_ids = list(map(lambda x: x['game_id'], usergames))
    return games.get_by_id(game_ids, dbconnection=dbconnection)


@autodb
def set(user_id:int, game_id:int, status:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "INSERT INTO usergames (user_id, game_id, status) VALUES ({}, {}, {})".format(user_id, game_id, status))


@autodb
def get_game_stats(user_id:int, dbconnection:dbutils.DBConnection=None) -> dict:
    games = get(user_id, status=2, dbconnection=dbconnection)
    info = dict()
    info['total'] = 0
    info['sport_types'] = dict()
    info['beautiful'] = dict()
    for game in games:
        assert isinstance(game, Game)
        if game.sport_type() not in info:
            info[game.sport_type()] = 0
        info[game.sport_type()] += game.duration()
        info['total'] += game.duration()
        if game.sport_type() not in info['sport_types']:
            info['sport_types'][game.sport_type()] = game.sport_type(True).title()
    for key in {key for key in info if isinstance(key, int)}:
        info['beautiful'][key] = format_duration(info[key])
    info['beautiful']['total'] = format_duration(info['total'])
    return info