import time

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
    return list() if len(setstr) == 0 else setstr[1:-1].split(_set_delimiter)


def encode_set(setlist:list) -> str:
    return _set_delimiter + _set_delimiter.join(list(map(str, setlist))) + _set_delimiter if len(setlist) > 0 else ''


class Cache:
    def __init__(self, lifetime:int):
        self._cache = dict()  # key -> (timestamp, value)
        self._lifetime = lifetime

    def __call__(self, func):  # as decarator
        self._func = func
        return self.cache

    def check(self, key) -> bool:
        retval = key in self._cache and time.time() - self._cache[key][0] <= self._lifetime
        return retval

    def get(self, key):
        return self._cache[key][1]

    def set(self, key, value):
        self._cache[key] = (time.time(), value)

    def cache(self, *args, **kwargs):
        raise NotImplementedError


class SimpleCache(Cache):
    def __init__(self, lifetime:int, id_attr:str):
        super().__init__(lifetime)
        self._id_attr = id_attr

    def cache(self, *args, **kwargs):
        some_key = args[0]

        if isinstance(some_key, str) and len(some_key.split(',')) > 0:
            some_key = splitstrlist(some_key)
            if len(some_key) == 1:
                some_key = some_key[0]

        if isinstance(some_key, list):
            key_ids = map(int, some_key)
            unknown = list()
            response = list()
            for some_key in key_ids:
                if not self.check(some_key):
                    unknown.append(some_key)
                else:
                    response.append(self.get(some_key))
            if len(unknown) > 0:
                retval = self._func(unknown, dbconnection=kwargs.get('dbconnection', None))
                for obj in retval:
                    self.set(getattr(obj, self._id_attr)(), obj)
                    response.append(obj)
            return response

        if isinstance(some_key, int):
            if self.check(some_key):
                return self.get(some_key)
            else:
                retval = self._func(some_key, dbconnection=kwargs.get('dbconnection', None))
                self.set(some_key, retval)
                return retval