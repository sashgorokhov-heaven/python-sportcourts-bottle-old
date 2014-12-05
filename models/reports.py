from models import autodb
import dbutils
import cacher


#@cacher.create_table_name('reports', 'game_id', 600, cacher.KeyCache)
@autodb
def reported(game_id:int, dbconnection:dbutils.DBConnection=None) -> bool:
    dbconnection.execute("SELECT COUNT(user_id) FROM reports WHERE game_id={}".format(game_id))
    return dbconnection.last()[0][0] > 0


@autodb
def report(game_id:int, user_id:int, status:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "INSERT INTO reports (game_id, user_id, status) VALUES ({}, {}, {})".format(game_id, user_id, status))
#    cacher.drop_by_table_name('reports', 'game_id', game_id)


@autodb
def report_unregistered(game_id:int, status:int, name:str, phone:str, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute(
        "INSERT INTO reports (game_id, status, name, phone) VALUES ({}, {}, '{}', '{}')".format(game_id, status, name,
                                                                                                phone))
#    cacher.drop_by_table_name('reports', 'game_id', game_id)


@autodb
def report_additional_charges(game_id:int, description:str, cost:int, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("INSERT INTO additional_charges VALUES ({}, '{}', {})".format(game_id, description, cost))


#@cacher.create('reports', 600, cacher.KeyCache)
@autodb
def get(game_id:int, dbconnection:dbutils.DBConnection=None) -> dict:
    # registered: user_id:int -> status:int, unregistered: name:str -> (status:int, phone:str)
    resp = {'registered': dict(), 'unregistered': dict(), 'additional':list()}
    dbconnection.execute("SELECT user_id, status FROM reports WHERE user_id>0 AND game_id={}".format(game_id))
    if len(dbconnection.last()) > 0:
        for user in dbconnection.last():
            user_id, status = user
            resp['registered'][user_id] = status
    dbconnection.execute("SELECT name, phone, status FROM reports WHERE user_id=0 AND game_id={}".format(game_id))
    if len(dbconnection.last()) > 0:
        for user in dbconnection.last():
            name, phone, status = user[0], user[1], user[2]
            resp['unregistered'][name] = (status, phone)
    dbconnection.execute("SELECT description, cost FROM additional_charges WHERE game_id={}".format(game_id))
    if len(dbconnection.last()) > 0:
        for i in dbconnection.last():
            resp['additional'].append(i)
    return resp