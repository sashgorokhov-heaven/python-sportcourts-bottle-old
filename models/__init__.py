import json
from modules.dbutils import DBConnection


def autodb(func):
    def wrapper(*args, **kwargs):
        mydb = False
        if 'dbconnection' not in kwargs or ('dbconnection' in kwargs and not kwargs['dbconnection']):
            mydb = True
            kwargs['dbconnection'] = DBConnection()
        try:
            result = func(*args, **kwargs)
        finally:
            if mydb:
                kwargs['dbconnection'].close()
        return result

    return wrapper


class JsonDBData(dict):
    def __init__(self, data=None):
        super().__init__()
        if data:
            self._data = json.loads(data)
        else:
            self._data = dict()

    def _get(self, key:str):
        return self._data[key]

    def _set(self, key:str, value):
        self._data[key] = value

    def __getitem__(self, item):
        return self._get(item)

    def __setitem__(self, key, value):
        return self._set(key, value)

    def format(self):
        return json.dumps(self._data)

    def __str__(self):
        return str(self._data)


def splitstrlist(line:str) -> list:
    return list(map(int, filter(lambda x: x != '', map(lambda x: x.strip(), line.split(',')))))