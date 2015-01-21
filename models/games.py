import dbutils
from models import autodb, splitstrlist, notifications, notificating
from modules.utils import format_duration
from objects import Game
from modules import create_link, utils
import cacher


games_cache = cacher.create_table_name('games', 'game_id', 600, cacher.SimpleCache, 'game_id')


@games_cache
@autodb
def get_by_id(game_id, dbconnection:dbutils.DBConnection=None) -> Game:
    if isinstance(game_id, str) and len(game_id.split(',')) > 0:
        game_id = splitstrlist(game_id)
        if len(game_id) == 1:
            game_id = game_id[0]

    if isinstance(game_id, list) and len(game_id) == 0: return list()

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


def get_all(dbconnection:dbutils.DBConnection=None) -> Game:
    dbconnection.execute("SELECT * FROM games WHERE deleted=0", dbutils.dbfields['games'])
    if len(dbconnection.last()) == 0: return list()
    return list(map(lambda x: Game(x, dbconnection), dbconnection.last()))


@autodb
def usergames_set(user_id:int, game_id:int, status:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("SELECT COUNT(*) FROM usergames WHERE user_id={} AND game_id={}".format(user_id, game_id))
    if dbconnection.last()[0][0] == 0:
        sql = "INSERT INTO usergames (user_id, game_id, status) VALUES ({}, {}, {})".format(user_id, game_id, status)
    else:
        sql = "UPDATE usergames SET status={} WHERE user_id={} AND game_id={}".format(status, user_id, game_id)
    dbconnection.execute(sql)
    games_cache.drop(game_id)
    cacher.drop_by_table_name('usergames', 'game_id', game_id)


@autodb
def usergames_reserve(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    usergames_set(user_id, game_id, 1, dbconnection=dbconnection)


@autodb
def usergames_subscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    usergames_set(user_id, game_id, 2, dbconnection=dbconnection)


@autodb
def usergames_unsubscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    usergames_set(user_id, game_id, 0, dbconnection=dbconnection)


@autodb
def subscribe(user_id:int, game_id:int, reserved:bool=False, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("SELECT status FROM usergames WHERE user_id={} AND game_id={}".format(user_id, game_id))
    if len(dbconnection.last()) == 0:
        if reserved:
            usergames_reserve(user_id, game_id, dbconnection=dbconnection)
        else:
            usergames_subscribe(user_id, game_id, dbconnection=dbconnection)
    else:
        status = dbconnection.last()[0][0]
        if status == 2 or status == 1 and reserved:
            return
        if (status == 1 or status == 0) and not reserved:
            usergames_subscribe(user_id, game_id, dbconnection=dbconnection)
            write_future_notifications(user_id, game_id, dbconnection=dbconnection)
        if status == 0 and reserved:
            usergames_reserve(user_id, game_id, dbconnection=dbconnection)


@autodb
def write_future_notifications(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    game = get_by_id(game_id, dbconnection=dbconnection)
    if not game.datetime.tommorow and not game.datetime.today:
        message = 'До игры "{}" осталось 2 дня!'.format(create_link.game(game))
        utils.spool_func(notificating.site.subscribed, user_id, message, 0, game_id, 'TIMESTAMP("{}")-INTERVAL 2 DAY'.format(game.datetime))
    if not game.datetime.today:
        message = 'Завтра состоится игра "{}"<br>Не пропустите!'.format(create_link.game(game))
        utils.spool_func(notificating.site.subscribed, user_id, message, 0, game_id, 'TIMESTAMP("{}")-INTERVAL 1 DAY'.format(game.datetime))


@autodb
def unsubscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("SELECT status FROM usergames WHERE user_id={} AND game_id={}".format(user_id, game_id))
    if len(dbconnection.last()) == 0:
        return
    status = dbconnection.last()[0][0]
    if status == 2 or status == 1:
        if status == 2:
            delete_future_notifications(user_id, game_id, dbconnection=dbconnection)
        usergames_unsubscribe(user_id, game_id, dbconnection=dbconnection)
    elif status == 0:
        return

    game = get_by_id(game_id, dbconnection=dbconnection)
    if game.reserved() > 0 and len(game.reserved_people()) > 0:
        for user_id in game.reserved_people():
            utils.spool_func(notificating.site.subscribed, user_id, 'В игре "{}" освободилось место!'.format(create_link.game(game)), 1, game_id)
            utils.spool_func(notificating.mail.tpl.notify_reserved, game, user_id)

@autodb
def delete_future_notifications(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "SELECT notification_id FROM notifications WHERE type=1 AND game_id={} AND user_id={} AND DATETIME>NOW()".format(game_id, user_id))
    if len(dbconnection.last()) == 0:
        return
    notifications.delete(list(map(lambda x: x[0], dbconnection.last())))


@autodb
def get_recent(court_id:int=0, city_id:int=1, sport_type:int=0, count:slice=slice(0, 20), old:bool=False,
               dbconnection:dbutils.DBConnection=None) -> list:
    sql = "SELECT * FROM games WHERE {} ORDER BY DATETIME {} LIMIT {}, {}"
    where = list()
    where.append("city_id={}".format(city_id))
    where.append("deleted=0")
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
    dbconnection.execute("UPDATE games SET deleted=1 WHERE game_id={}".format(game_id))
    games_cache.drop(game_id)


@autodb
def court_game_intersection(court_id:int, datetime:str, duration:int, dbconnection:dbutils.DBConnection=None) -> Game:
    sql = (" SELECT * FROM games WHERE court_id='{court_id}'"
           " AND deleted=0 AND ("
           " (datetime BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE)"
           " OR "
           " (datetime + INTERVAL duration MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE))"
           " AND "
           " datetime!='{datetime}' AND datetime!=('{datetime}' + INTERVAL '{duration}' MINUTE)"
           " AND "
           " (datetime + INTERVAL duration MINUTE)!='{datetime}' AND (datetime + INTERVAL duration MINUTE)!=('{datetime}' + INTERVAL '{duration}' MINUTE)")
    sql = sql.format(court_id=court_id, datetime=datetime, duration=duration)
    dbconnection.execute(sql, dbutils.dbfields['games'])
    if len(dbconnection.last()) > 0:
        return Game(dbconnection.last()[0], dbconnection=dbconnection)
    return None


@autodb
def user_game_intersection(user_id:int, game:Game, dbconnection:dbutils.DBConnection=None) -> Game:
    sql = (" SELECT * FROM games WHERE game_id!='{game_id}'"
           " AND game_id IN (SELECT game_id FROM usergames WHERE user_id='{user_id}' AND status=2)"
           " AND deleted=0 AND ("
           " (datetime BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE)"
           " OR "
           " (datetime + INTERVAL duration MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL '{duration}' MINUTE))"
           " AND "
           " datetime!='{datetime}' AND datetime!=('{datetime}' + INTERVAL '{duration}' MINUTE)"
           " AND "
           " (datetime + INTERVAL duration MINUTE)!='{datetime}' AND (datetime + INTERVAL duration MINUTE)!=('{datetime}' + INTERVAL '{duration}' MINUTE)")
    sql = sql.format(datetime=game.datetime, duration=game.duration(), user_id=user_id, game_id=game.game_id())
    dbconnection.execute(sql, dbutils.dbfields['games'])
    if len(dbconnection.last()) > 0:
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
    games_cache.drop(game_id)


@cacher.create_table_name('reports', 'user_id', 600, cacher.KeyCache)
@autodb
def get_user_played_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT game_id FROM reports WHERE user_id='{}' AND status>0".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last()) > 0 else list()


@autodb
def get_subscribed_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT game_id FROM usergames WHERE user_id='{}' AND status=2".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last()) > 0 else list()


@autodb
def get_unsubscribed_users(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    return dbconnection.execute("SELECT user_id, datetime FROM usergames WHERE game_id='{}' AND status=0 ORDER BY datetime DESC".format(game_id))


@cacher.create_table_name('usergames', 'game_id', 600, cacher.KeyCache)
@autodb
def get_subscribed_to_game(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT user_id FROM usergames WHERE game_id='{}' AND status=2".format(game_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last()) > 0 else list()


@cacher.create_table_name('usergames', 'game_id', 600, cacher.KeyCache)
@autodb
def get_reserved_to_game(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT user_id FROM usergames WHERE game_id='{}' AND status=1".format(game_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last()) > 0 else list()


@autodb
def get_responsible_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT game_id FROM games WHERE responsible_user_id='{}' and deleted=0".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last()) > 0 else list()


@autodb
def get_organizer_games(user_id:int, dbconnection:dbutils.DBConnection=None) -> list():
    dbconnection.execute("SELECT game_id FROM games WHERE created_by='{}' and deleted=0".format(user_id))
    return list(map(lambda x: x[0], dbconnection.last())) if len(dbconnection.last()) > 0 else list()


@cacher.create('game_stats_cache', 600, cacher.KeyCache)
@autodb
def get_game_stats(user_id:int, dbconnection:dbutils.DBConnection=None) -> dict:
    sql = "SELECT game_id, status FROM reports WHERE user_id={} AND STATUS=2".format(user_id)
    usergames = dbconnection.execute(sql)
    game_ids = list(map(lambda x: x[0], usergames)) if len(usergames) != 0 else list()
    games = get_by_id(game_ids, dbconnection=dbconnection)
    info = dict()
    info['total'] = 0
    info['sport_types'] = dict()
    info['beautiful'] = dict()
    assert isinstance(games, list)
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