import dbutils
from models import autodb
from objects import Amplua


@autodb
def get(amplua_id, dbconnection:dbutils.DBConnection=None) -> Amplua:
    if isinstance(amplua_id, list) and len(amplua_id)==0: return list()

    if isinstance(amplua_id, int) and amplua_id != 0:
        dbconnection.execute("SELECT * FROM ampluas WHERE amplua_id='{}'".format(amplua_id), dbutils.dbfields['ampluas'])
    elif isinstance(amplua_id, list):
        dbconnection.execute("SELECT * FROM ampluas WHERE amplua_id IN (" + ','.join(map(str, amplua_id)) + ")",
                             dbutils.dbfields['ampluas'])
    elif amplua_id == 0:
        dbconnection.execute("SELECT * FROM ampluas", dbutils.dbfields['ampluas'])

    if len(dbconnection.last()) == 0: return list()

    ampluas = dbconnection.last()
    ampluas = list(map(lambda x: Amplua(x, dbconnection=dbconnection), ampluas))

    if isinstance(amplua_id, int) and amplua_id != 0:
        return ampluas[0]
    elif isinstance(amplua_id, list) or amplua_id == 0:
        return ampluas


#@autodb
#def parse(ampluas_str:str, detalized:bool=False, dbconnection:dbutils.DBConnection=None):
#    if len(ampluas_str)==0:
#        return list() if detalized else set()
#    ampluas = list(map(int, decode_set(ampluas_str)))
#    return get(ampluas, dbconnection=dbconnection) if detalized else set(ampluas)