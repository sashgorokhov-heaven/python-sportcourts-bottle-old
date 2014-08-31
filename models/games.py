from models import autodb, splitstrlist, cities, courts, game_types, sport_types, users
from modules import dbutils
from modules.utils import beautifuldate, beautifultime, beautifulday


@autodb
def detalize_game(game:dict, detalized:bool=False, dbconnection:dbutils.DBConnection=None):
    if 'city_id' in game and detalized:
        game['city'] = cities.get(game['city_id'], dbconnection=dbconnection)
        game.pop('city_id')

    if 'court_id' in game and detalized:
        game['court'] = courts.get(game['court_id'], dbconnection=dbconnection)
        game.pop('court_id')

    if 'game_type' in game and detalized:
        game['game_type'] = game_types.get(game['game_type'], dbconnection=dbconnection)

    if 'sport_type' in game and detalized:
        game['sport_type'] = sport_types.get(game['sport_type'], dbconnection=dbconnection)

    if 'datetime' in game:
        dbutils.strdates(game)
        game['parsed_datetime'] = (
        beautifuldate(game['datetime']), beautifultime(game['datetime']), beautifulday(game['datetime']))

    if 'subscribed' in game and detalized:
        subscribed = game['subscribed'].split('|')[1:-1]
        if len(subscribed) > 0:
            _users = users.get(subscribed, fields=['user_id', 'first_name', 'last_name', 'phone'],
                               dbconnection=dbconnection)
            game['subscribed'] = {'count': len(_users), 'users': _users}
        else:
            game['subscribed'] = {'count': 0, 'users': list()}


@autodb
def get_by_id(game_id, detalized:bool=False, fields:list=dbutils.dbfields['games'],
              dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['games'] if i in set(fields)]
    select = ','.join(orderedfields)

    if isinstance(game_id, str) and len(game_id.split(',')) > 0:
        game_id = splitstrlist(game_id)
        if len(game_id) == 1:
            game_id = game_id[0]

    if isinstance(game_id, int):
        dbconnection.execute("SELECT " + select + " FROM games WHERE game_id={}".format(game_id), orderedfields)
    elif isinstance(game_id, list):
        dbconnection.execute("SELECT " + select + " FROM games WHERE game_id IN (" + ','.join(map(str, game_id)) + ")",
                             orderedfields)

    games = dbconnection.last()
    for game in games:
        detalize_game(game, detalized=detalized, dbconnection=dbconnection)

    if isinstance(game_id, int):
        return games[0]
    elif isinstance(game_id, list):
        return games


@autodb
def subscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    subscribed = dbconnection.execute("SELECT subscribed FROM games WHERE game_id='{}'".format(game_id))[0][0]
    subscribed = list(map(int, subscribed.split('|')[1:-1]))
    if user_id in set(subscribed):
        raise ValueError("User <{}> already subscibed".format(user_id))
    subscribed.append(user_id)
    if len(subscribed) > 0:
        subscribed = '|' + '|'.join(map(str, subscribed)) + '|'
    else:
        subscribed = ''
    dbconnection.execute("UPDATE games SET subscribed='{}' WHERE game_id={}".format(subscribed, game_id))


@autodb
def unsubscribe(user_id:int, game_id:int, dbconnection:dbutils.DBConnection=None):
    subscribed = dbconnection.execute("SELECT subscribed FROM games WHERE game_id='{}'".format(game_id))[0][0]
    subscribed = list(map(int, subscribed.split('|')[1:-1]))
    if user_id not in set(subscribed):
        raise ValueError("User <{}> not subscibed".format(user_id))
    subscribed.remove(user_id)
    if len(subscribed) > 0:
        subscribed = '|' + '|'.join(map(str, subscribed)) + '|'
    else:
        subscribed = ''
    dbconnection.execute("UPDATE games SET subscribed='{}' WHERE game_id={}".format(subscribed, game_id))


@autodb
def get_recent(court_id:int=0, city_id:int=1, sport_type:int=0, count:slice=slice(0, 20), detalized:bool=False,
               fields:list=dbutils.dbfields['games'], dbconnection:dbutils.DBConnection=None) -> list:
    orderedfields = [i for i in dbutils.dbfields['games'] if i in set(fields)]
    select = ','.join(orderedfields)

    sql = "SELECT " + select + " FROM games WHERE {} ORDER BY datetime ASC LIMIT {}, {}"
    where = list()
    where.append("city_id={}".format(city_id))
    where.append("datetime + INTERVAL duration MINUTE>NOW()")
    if court_id:
        where.append("court_id={}".format(court_id))
    if sport_type:
        where.append("sport_type={}".format(sport_type))
    sql = sql.format(' AND '.join(where), count.start if count.start else 0, count.stop)

    games = dbconnection.execute(sql, orderedfields)

    for game in games:
        detalize_game(game, detalized=detalized, dbconnection=dbconnection)

    return games


@autodb
def delete(game_id:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("DELETE FROM games WHERE game_id={}".format(game_id))


@autodb
def intersection(court_id:int, datetime:str, duration:int, dbconnection:dbutils.DBConnection=None):
    sql = """\
        SELECT game_id FROM games WHERE court_id={court_id} AND (\
        (DATETIME BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE) OR \
        (DATETIME + INTERVAL {duration} MINUTE BETWEEN '{datetime}' AND '{datetime}' + INTERVAL {duration} MINUTE));\
        """.format(
        court_id=court_id,
        datetime=datetime,
        duration=duration)
    dbconnection.execute(sql)
    if len(dbconnection.last()) == 0:
        return 0
    return dbconnection.last()[0][0]


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
        ', '.join(['{}="{}"'.format(i, kwargs[i]) for i in kwargs]),
        game_id)
    dbconnection.execute(sql)


@autodb
def get_user_games(user_id:int, detalized:bool=False, fields:list=dbutils.dbfields['games'],
                   dbconnection:dbutils.DBConnection=None):
    orderedfields = [i for i in dbutils.dbfields['games'] if i in set(fields)]
    select = ','.join(orderedfields)

    dbconnection.execute("SELECT " + select + " FROM games WHERE LOCATE('|{}|', subscribed)".format(user_id),
                         orderedfields)

    if len(dbconnection.last()) == 0:
        return list()

    for game in dbconnection.last():
        detalize_game(game, detalized=detalized, dbconnection=dbconnection)

    return dbconnection.last()