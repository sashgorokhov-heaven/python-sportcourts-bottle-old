from models import autodb, splitstrlist, sport_types
from modules import dbutils


def get(amplua_id, dbconnection:dbutils.DBConnection=None):
    if isinstance(amplua_id, str) and len(amplua_id.split(',')) > 0:
        amplua_id = splitstrlist(amplua_id)
        if len(amplua_id) == 1:
            amplua_id = amplua_id[0]

    if isinstance(amplua_id, int) and amplua_id != 0:
        dbconnection.execute("SELECT * FROM ampluas WHERE amplua_id='{}'".format(amplua_id), dbutils.dbfields['ampluas'])
    elif isinstance(amplua_id, list):
        dbconnection.execute("SELECT * FROM ampluas WHERE amplua_id IN (" + ','.join(map(str, amplua_id)) + ")",
                             dbutils.dbfields['ampluas'])
    elif amplua_id == 0:
        dbconnection.execute("SELECT * FROM ampluas", dbutils.dbfields['ampluas'])

    if len(dbconnection.last()) == 0:
        return list()

    ampluas = dbconnection.last()

    _sport_types = {sport_type['sport_id']:sport_type for sport_type in sport_types.get(list(map(lambda x: x['sport_type'], ampluas)), dbconnection=dbconnection)}

    for amplua in ampluas:
        amplua['sport_type'] = _sport_types[amplua['sport_type']]

    if isinstance(amplua_id, int) and amplua_id != 0:
        return ampluas[0]
    elif isinstance(amplua_id, list) or amplua_id == 0:
        return ampluas


@autodb
def parse(ampluas_str:str, detalized:bool=False, dbconnection:dbutils.DBConnection=None):
    if len(ampluas_str)==0:
        return list() if detalized else set()
    ampluas = list(map(int, ampluas_str.split('|')[1:-1]))
    return get(ampluas, dbconnection=dbconnection) if detalized else set(ampluas)