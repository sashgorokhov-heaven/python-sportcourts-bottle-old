from models import autodb, games
from modules import dbutils


@autodb
def get(user_id:int, status:int=-1, detalized:bool=False, fields:list=dbutils.dbfields['games'],
        dbconnection:dbutils.DBConnection=None) -> list:  # list of dict
    usergames = dbconnection.execute("SELECT game_id, status FROM usergames WHERE user_id={}{}".format(user_id,
                                                                                                       '' if status < 0 else " AND status={}".format(
                                                                                                           status)),
                                     ['game_id', 'status'])
    if not detalized:
        return usergames
    game_ids = list(map(lambda x: x['game_id'], usergames))
    if len(game_ids) == 0:
        return list()
    return games.get_by_id(game_ids, detalized=True, fields=fields, dbconnection=dbconnection)


@autodb
def set(user_id:int, game_id:int, status:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "INSERT INTO usergames (user_id, game_id, status) VALUES ({}, {}, {})".format(user_id, game_id, status))


def format_duration(duration:int) -> tuple:
    postfix = 'минут'
    prefix = int(str(duration)[-1])
    if prefix == 0 or 5 <= prefix <= 9:
        postfix = 'минут'
    elif prefix == 1:
        postfix = 'минута'
    elif 2 <= prefix <= 4:
        postfix = 'минуты'
    if duration > 60:
        duration = round(duration / 60)
        prefix = int(str(duration)[-1])
        if prefix == 0 or 5 <= prefix <= 9:
            postfix = 'часов'
        elif prefix == 1:
            postfix = 'час'
        elif 2 <= prefix <= 4:
            postfix = 'часа'
        if duration > 24:
            duration = round(duration / 24)
            prefix = int(str(duration)[-1])
            if prefix == 0 or 5 <= prefix <= 9:
                postfix = 'дней'
            elif prefix == 1:
                postfix = 'день'
            elif 2 <= prefix <= 4:
                postfix = 'дня'
    return str(duration), postfix


@autodb
def get_game_stats(user_id:int, dbconnection:dbutils.DBConnection=None) -> dict:
    games = get(user_id, status=2, detalized=True, fields=['sport_type', 'duration'],
                dbconnection=dbconnection)
    info = dict()
    info['total'] = 0
    info['sport_types'] = dict()
    info['beautiful'] = dict()
    for game in games:
        if game['sport_type']['sport_id'] not in info:
            info[game['sport_type']['sport_id']] = 0
        info[game['sport_type']['sport_id']] += game['duration']
        info['total'] += game['duration']
        if game['sport_type']['sport_id'] not in info['sport_types']:
            info['sport_types'][game['sport_type']['sport_id']] = game['sport_type']['title']
    for key in {key for key in info if isinstance(key, int)}:
        info['beautiful'][key] = format_duration(info[key])
    info['beautiful']['total'] = format_duration(info['total'])
    return info