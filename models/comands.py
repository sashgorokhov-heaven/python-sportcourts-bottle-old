import dbutils
from models import autodb
from objects import Comand


@autodb
def get_comand_ids(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT comand_id FROM comands WHERE game_id='{}'".format(game_id))
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: x[0], dbconnection.last()))


@autodb
def get_comands(comand_id:(list, int), dbconnection:dbutils.DBConnection=None) -> Comand:
    if isinstance(comand_id, list) and len(comand_id)==0: return list()

    if isinstance(comand_id, int):
        dbconnection.execute("SELECT * FROM comands WHERE comand_id='{}'".format(comand_id))
    elif isinstance(comand_id, list):
        dbconnection.execute("SELECT * FROM comands WHERE comand_id in ({})".format(','.join(list(map(str, comand_id)))))

    return list(map(lambda x: Comand(x, dbconnection), dbconnection.last()))


@autodb
def get_subscribed(command_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT user_id FROM usergames WHERE comand_id='{}'".format(command_id))
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: x[0], dbconnection.last()))