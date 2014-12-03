import time


def splitstrlist(line:str) -> list:
    return list(map(int, filter(lambda x: x != '', map(lambda x: x.strip(), line.split(',')))))


_instances = dict() # cache_key -> Cache
_table_name_instances = dict() # table_name -> { accept_key -> [ _Cache ] }


def drop(cache_key:str, value_key=None):
    if cache_key not in _instances:
        raise KeyError('Cache class for <{}> not found'.format(cache_key))
    if value_key:
        _instances[cache_key].drop(value_key)
    else:
        _instances[cache_key].dropall()


def keys():
    return _instances.keys()


def drop_by_table_name(table_name:str, accept_key:str, value_key=None):
    if table_name in _table_name_instances:
        if accept_key in _table_name_instances[table_name]:
            for cache in _table_name_instances[table_name][accept_key]:
                if value_key:
                    cache.drop(value_key)
                else:
                    cache.dropall()
        else:
            for accept_key in _table_name_instances[table_name]:
                for cache in _table_name_instances[table_name][accept_key]:
                    cache.dropall()


def dropall():
    for cache_key in _instances:
        drop(cache_key)
    for table_name in _table_name_instances:
        for accept_key in _table_name_instances[table_name]:
            drop_by_table_name(table_name, accept_key)


class _Cache:
    def __init__(self, lifetime:int):
        self._cache = dict()  # key -> (timestamp, value)
        self.lifetime = lifetime

    def __call__(self, func):  # as decarator
        self._func = func
        return self.cache

    def check(self, key) -> bool:
        if key in self._cache:
            if time.time() - self._cache[key][0] <= self.lifetime:
                return True
            self.drop(key)
        return False

    def get(self, key):
        return self._cache[key][1]

    def set(self, key, value):
        self._cache[key] = (time.time(), value)

    def drop(self, key):
        if key in self._cache:
            self._cache.pop(key)

    def dropall(self):
        self._cache.clear()

    def cache(self, *args, **kwargs):
        raise NotImplementedError


def get(table_name:str, accept_key:str) -> _Cache:
    return _table_name_instances[table_name][accept_key]

class SimpleCache(_Cache):
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
                retval = self._func(unknown, *args[1:], **kwargs)
                for obj in retval:
                    self.set(getattr(obj, self._id_attr)(), obj)
                    response.append(obj)
            return response

        if isinstance(some_key, int):
            if self.check(some_key):
                return self.get(some_key)
            else:
                retval = self._func(some_key, *args[1:], **kwargs)
                self.set(some_key, retval)
                return retval

        raise TypeError('Unkown type of first argument <{}>'.format(some_key.__class__.__name__))


class KeyCache(_Cache):
    def cache(self, *args, **kwargs):
        key = args[0]
        if self.check(key):
            return self.get(key)
        retval = self._func(key, *args[1:], **kwargs)
        self.set(key, retval)
        return retval


def create(cache_key:str, lifetime:int, cache_class:_Cache=SimpleCache, *args) -> _Cache:
    if cache_key in _instances:
        raise KeyError('Dublicate cache key for <{}>'.format(cache_key))
    _instances[cache_key] = cache_class(lifetime, *args)
    return _instances[cache_key]


def create_table_name(table_name:str, accept_key:str, lifetime:int, cache_class:_Cache, *args) -> _Cache:
    if table_name in _table_name_instances:
        if accept_key in _table_name_instances[table_name]:
            _table_name_instances[table_name][accept_key].append(cache_class(lifetime, *args))
        else:
            _table_name_instances[table_name][accept_key] = [cache_class(lifetime, *args)]
    else:
        _table_name_instances[table_name] = {accept_key:[cache_class(lifetime, *args)]}
    return _table_name_instances[table_name][accept_key][-1]