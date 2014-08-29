from modules.dbutils import DBConnection


def autodb(func):
    def wrapper(*args, **kwargs):
        mydb = False
        if 'dbconnection' not in kwargs:
            mydb = True
            kwargs['dbconnection'] = DBConnection()
        try:
            result = func(*args, **kwargs)
        finally:
            if mydb:
                kwargs['dbconnection'].close()
        return result

    return wrapper


def splitstrlist(line:str) -> list:
    return list(map(int, filter(lambda x: x != '', map(lambda x: x.strip(), line.split(',')))))