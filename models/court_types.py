import dbutils
from models import autodb, splitstrlist
from objects import CourtType
import cacher


@cacher.create('court_types', 600, cacher.SimpleCache, 'type_id')
@autodb
def get(type_id, dbconnection:dbutils.DBConnection=None) -> list:
    if isinstance(type_id, str) and len(type_id.split(',')) > 0:
        type_id = splitstrlist(type_id)
        if len(type_id) == 1:
            type_id = type_id[0]

    if isinstance(type_id, list) and len(type_id) == 0: return list()

    if isinstance(type_id, int) and type_id != 0:
        dbconnection.execute("SELECT * FROM court_types WHERE type_id='{}'".format(type_id),
                             dbutils.dbfields['court_types'])
    elif isinstance(type_id, list):
        dbconnection.execute(
            "SELECT * FROM court_types WHERE type_id IN (" + ','.join(map(str, type_id)) + ")",
            dbutils.dbfields['court_types'])
    elif type_id == 0:
        dbconnection.execute("SELECT * FROM court_types", dbutils.dbfields['court_types'])

    if len(dbconnection.last()) == 0: return list()

    court_types = dbconnection.last()
    court_types = list(map(lambda x: CourtType(x), court_types))

    if isinstance(type_id, int) and type_id != 0:
        return court_types[0]
    elif isinstance(type_id, list) or type_id == 0:
        return court_types