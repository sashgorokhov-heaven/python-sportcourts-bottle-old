import dbutils
from models import autodb, games
from objects import Game
from modules.utils import format_duration


@autodb
def get(user_id:int, status:int, dbconnection:dbutils.DBConnection=None) -> list:
    sql = "SELECT game_id, status FROM usergames WHERE user_id={} AND STATUS={}"
    usergames = dbconnection.execute(sql.format(user_id, status))
    if len(usergames) == 0: return list()
    game_ids = list(map(lambda x: x[0], usergames))
    return games.get_by_id(game_ids, dbconnection=dbconnection)


@autodb
def set(user_id:int, game_id:int, status:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("SELECT COUNT(*) FROM usergames WHERE user_id={} AND game_id={}".format(user_id, game_id))
    if dbconnection.last()[0][0] == 0:
        sql = "INSERT INTO usergames (user_id, game_id, status) VALUES ({}, {}, {})".format(user_id, game_id, status)
    else:
        sql = "UPDATE usergames SET status={} WHERE user_id={} AND game_id={}".format(status, user_id, game_id)
    dbconnection.execute(sql)


@autodb
def reserve(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    set(user_id, game_id, 1, dbconnection=dbconnection)


@autodb
def subscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    set(user_id, game_id, 2, dbconnection=dbconnection)


@autodb
def unsubscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    set(user_id, game_id, 0, dbconnection=dbconnection)


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