import dbutils
from models import autodb
import modules

@autodb
def create(email:str, dbconnection:dbutils.DBConnection=None) -> str:
    dbconnection.execute("SELECT activated, token FROM activation WHERE email='{}'".format(email))
    if len(dbconnection.last())>0:
        if dbconnection.last()[0][0]==1:
            raise ValueError('{} already activated'.format(email), email, dbconnection.last()[0][1])
        elif dbconnection.last()[0][0]==2:
            raise KeyError('{} already registrated'.format(email), email)
        else:
            dbconnection.execute("DELETE FROM activation WHERE email='{}'".format(email))
    token = modules.generate_token()
    dbconnection.execute("INSERT INTO activation (email, token) VALUES ('{}', '{}')".format(email, token))
    return token


@autodb
def activate(email:str, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("UPDATE activation SET activated=1 WHERE email='{}'".format(email))


@autodb
def get(token:str, dbconnection:dbutils.DBConnection=None) -> str:
    dbconnection.execute("SELECT email FROM activation WHERE token='{}'".format(token))
    if len(dbconnection.last())==0:
        raise ValueError('No email for <{}>'.format(token))
    return dbconnection.last()[0][0]


def status(email:str, dbconnection:dbutils.DBConnection=None) -> int:
    return dbconnection.execute("SELECT activated FROM activation WHERE email='{}'".format(email))[0][0]