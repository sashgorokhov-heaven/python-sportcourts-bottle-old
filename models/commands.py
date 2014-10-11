import dbutils
from models import autodb
from objects import Command


@autodb
def get_command_ids(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT comand_id FROM commands WHERE game_id='{}'".format(game_id))
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: x[0], dbconnection.last()))


@autodb
def get_commands(command_id:(list, int), dbconnection:dbutils.DBConnection=None) -> Command:
    if isinstance(command_id, list) and len(command_id)==0: return list()

    if isinstance(command_id, int):
        dbconnection.execute("SELECT * FROM commands WHERE comand_id='{}'".format(command_id))
    elif isinstance(command_id, list):
        dbconnection.execute("SELECT * FROM commands WHERE comand_id in ({})".format(','.join(list(map(str, command_id)))))

    return list(map(lambda x: Command(x, dbconnection), dbconnection.last()))


@autodb
def get_subscribed(command_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT user_id FROM usergames WHERE command_id='{}'".format(command_id))
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: x[0], dbconnection.last()))