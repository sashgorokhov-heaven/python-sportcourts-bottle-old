from dbutils import DBConnection


def autodb(func):
    def wrapper(*args, **kwargs):
        mydb = False
        if 'dbconnection' not in kwargs or \
                ('dbconnection' in kwargs and
                     (not kwargs['dbconnection'] or
                          (kwargs['dbconnection'] and kwargs['dbconnection'].closed))):
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


_set_delimiter = '|'


def decode_set(setstr:str) -> list:
    return list() if len(setstr)==0 else setstr[1:-1].split(_set_delimiter)


def encode_set(setlist:list) -> str:
    return _set_delimiter+_set_delimiter.join(list(map(str, setlist)))+_set_delimiter if len(setlist)>0 else ''