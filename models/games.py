import dbutils
from models import autodb, splitstrlist, notifications
from objects import Game
from modules import create_link


@autodb
def get_by_id(game_id, dbconnection:dbutils.DBConnection=None) -> Game:
    if isinstance(game_id, str) and len(game_id.split(',')) > 0:
        game_id = splitstrlist(game_id)
        if len(game_id) == 1:
            game_id = game_id[0]

    if isinstance(game_id, list) and len(game_id)==0: return list()

    if isinstance(game_id, int):
        dbconnection.execute("SELECT * FROM games WHERE game_id={}".format(game_id), dbutils.dbfields['games'])
    elif isinstance(game_id, list):
        dbconnection.execute("SELECT * FROM games WHERE game_id IN (" + ','.join(map(str, game_id)) + ")",
                             dbutils.dbfields['games'])

    if len(dbconnection.last()) == 0: return list()

    games = dbconnection.last()
    games = list(map(lambda x: Game(x, dbconnection=dbconnection), games))

    if isinstance(game_id, int):
        return games[0]
    elif isinstance(game_id, list):
        return games


@autodb
def subscribe(user_id:int, game_id:int, reserved:bool=False, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("SELECT status FROM usergames WHERE user_id={} AND game_id={}".format(user_id, game_id))
    if len(dbconnection.last())==0:
        dbconnection.execute("INSERT INTO usergames (user_id, game_id, status) VALUES ({}, {}, {})".format(user_id, game_id, -1))
    else:
        status = dbconnection.last()[0][0]
        if status==-1 or (status==-2 and reserved):
            raise ValueError("User <{}> already subscibed".format(user_id))
        elif status==-3 or status==-2:
            dbconnection.execute("UPDATE usergames SET status=-1 WHERE user_id={} AND game_id={}".format(user_id, game_id))
        else:
            raise ValueError('Unknown {}:{} status'.format(user_id, game_id))
    write_future_notifications(user_id, game_id, dbconnection=dbconnection)


@autodb
def write_future_notifications(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    game = get_by_id(game_id, dbconnection=dbconnection)
    if not game.datetime.tommorow and not game.datetime.today:
        message = 'До игры "{}" осталось 2 дня!'.format(create_link.game(game))
        notifications.add(user_id, message, 0, game_id, 1, 'TIMESTAMP("{}")-INTERVAL 2 DAY'.format(game.datetime))
    if not game.datetime.today:
        message = 'Завтра состоится игра "{}"<br>Не пропустите!'.format(create_link.game(game))
        notifications.add(user_id, message, 1, game_id, 1, 'TIMESTAMP("{}")-INTERVAL 1 DAY'.format(game.datetime))


@autodb
def unsubscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("SELECT status FROM usergames WHERE user_id={} AND game_id={}".format(user_id, game_id))
    if len(dbconnection.last())==0:
        raise ValueError("User <{}> not subscibed".format(user_id))
    else:
        status = dbconnection.last()[0][0]
        if status==-1:
            dbconnection.execute("UPDATE usergames SET status=-2 WHERE user_id={} AND game_id={}".format(user_id, game_id))
        elif status==-3:
            raise ValueError("User <{}> not subscibed".format(user_id))
        else:
            raise ValueError('Unknown {}:{} status'.format(user_id, game_id))
    delete_future_notifications(user_id, game_id, dbconnection=dbconnection)


@autodb
def delete_future_notifications(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "SELECT notification_id FROM notifications WHERE type=1 AND game_id={} AND DATETIME>NOW()".format(game_id))
    if len(dbconnection.last()) == 0:
        return
    notifications.delete(list(map(lambda x: x[0], dbconnection.last())))


@autodb
def get_recent(court_id:int=0, city_id:int=1, sport_type:int=0, count:slice=slice(0, 20), old:bool=False,
               dbconnection:dbutils.DBConnection=None) -> list:
    sql = "SELECT * FROM games WHERE {} ORDER BY datetime {} LIMIT {}, {}"
    where = list()
    where.append("city_id={}".format(city_id))
    where.append("datetime+INTERVAL duration MINUTE {} NOW()".format('>' if not old else '<'))
    if court_id:
        where.append("court_id={}".format(court_id))
    if sport_type:
        where.append("sport_type={}".format(sport_type))
    sql = sql.format(' AND '.join(where), 'ASC' if not old else 'DESC', count.start if count.start else 0, count.stop)

    games = dbconnection.execute(sql, dbutils.dbfields['games'])
    games = list(map(lambda x: Game(x, dbconnection=dbconnection), games))

    return games


@autodb
def delete(game_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("INSERT INTO deleted_games SELECT * FROM games WHERE game_id={}".format(game_id))
    dbconnection.execute("DELETE FROM games WHERE game_id={}".format(game_id))
    dbconnection.execute("DELETE FROM usergames WHERE game_id={}".format(game_id))
    dbconnection.execute("DELETE FROM notifications WHERE game_id={}".format(game_id))


@autodb
def court_game_intersection(court_id:int, datetime:str, duration:int, dbconnection:dbutils.DBConnection=None) -> Game:
    sql = (" SELECT * FROM games WHERE court_id='{court_id}'"
           " AND ("
           " (datetime BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE)"
           " OR "
           " (datetime + INTERVAL duration MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE))"
           " AND "
           " datetime!='{datetime}' AND datetime!=('{datetime}' + INTERVAL '{duration}' MINUTE)"
           " AND "
           " (datetime + INTERVAL duration MINUTE)!='{datetime}' AND (datetime + INTERVAL duration MINUTE)!=('{datetime}' + INTERVAL '{duration}' MINUTE)")
    sql = sql.format(court_id=court_id, datetime=datetime, duration=duration)
    dbconnection.execute(sql)
    if len(dbconnection.last()) > 0:
        return Game(dbconnection.last()[0], dbconnection=dbconnection)
    return None


def user_game_intersection(user_id:int, game:Game, dbconnection:dbutils.DBConnection=None) -> Game:
    sql = (" SELECT * FROM games WHERE game_id!='{game_id}'"
           " AND game_id in (SELECT game_id FROM usergames WHERE user_id='{user_id}' AND status=-1)"
           " AND ("
           " (datetime BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE)"
           " OR "
           " (datetime + INTERVAL duration MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE))"
           " AND "
           " datetime!='{datetime}' AND datetime!=('{datetime}' + INTERVAL '{duration}' MINUTE)"
           " AND "
           " (datetime + INTERVAL duration MINUTE)!='{datetime}' AND (datetime + INTERVAL duration MINUTE)!=('{datetime}' + INTERVAL '{duration}' MINUTE)")
    sql = sql.format(datetime=game.datetime, duration=game.duration(), user_id=user_id, game_id=game.game_id())
    dbconnection.execute(sql, dbutils.dbfields['games'])
    if len(dbconnection.last())>0:
        return Game(dbconnection.last()[0], dbconnection=dbconnection)
    return None


@autodb
def add(dbconnection:dbutils.DBConnection=None, **kwargs) -> int:
    sql = 'INSERT INTO games ({dbkeylist}) VALUES ({dbvaluelist})'
    keylist = list(kwargs.keys())
    sql = sql.format(
        dbkeylist=', '.join(keylist),
        dbvaluelist=', '.join(["'{}'".format(str(kwargs[key])) for key in keylist]))
    dbconnection.execute(sql)
    dbconnection.execute('SELECT last_insert_id() FROM games')
    return dbconnection.last()[0][0]


@autodb
def update(game_id:int, dbconnection:dbutils.DBConnection=None, **kwargs):
    sql = 'UPDATE games SET {} WHERE game_id={}'.format(
        ', '.join(["{}='{}'".format(i, kwargs[i]) for i in kwargs]),
        game_id)
    dbconnection.execute(sql)


@autodb
def get_user_played_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT game_id FROM usergames WHERE user_id='{}' AND status>0".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last())>0 else list()


@autodb
def get_subscribed_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT game_id FROM usergames WHERE user_id='{}' AND status=-1".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last())>0 else list()


@autodb
def get_subscribed_to_game(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT user_id FROM usergames WHERE game_id='{}' AND status>=-1".format(game_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last())>0 else list()

def get_reserved_to_game(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT user_id FROM usergames WHERE game_id='{}' AND status=-2".format(game_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last())>0 else list()

@autodb
def get_responsible_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT game_id FROM games WHERE responsible_user_id='{}'".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last())>0 else list()


@autodb
def get_organizer_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list():
    dbconnection.execute("SELECT game_id FROM games WHERE created_by='{}'".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last())>0 else list()