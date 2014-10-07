import datetime

import pymysql

import modules


class DBConnection:
    def __init__(self, **kwargs):
        if len(kwargs) == 0:
            self._db = pymysql.connect(host=modules.config['api']['db']['dbhost'],
                                       user=modules.config['api']['db']['dbuser'],
                                       passwd=modules.config['api']['db']['dbpasswd'],
                                       db=modules.config['api']['db']['dbname'],
                                       charset='utf8'
            )
        else:
            self._db = pymysql.connect(**kwargs)
        self._closed = False
        self._cursor = self._db.cursor()
        self._last = None

    def execute(self, query:str, mapnames:list=None) -> list:
        """
        Execute a SQL query
        :param query: SQL query
        :param mapnames: field names
        :return:  list of lines, where line is also a list of ordered database fields
        """
        if self._cursor.execute(query) == 0:
            self._last = list()
        else:
            data = self._cursor.fetchall()
            # люблю питон за такие моменты
            self._last = [dict(zip(mapnames, list(line))) if mapnames else list(line) for line in
                          data] if data else list()
        return self._last

    def last(self) -> list:
        return self._last

    @property
    def closed(self) -> bool:
        return self._closed

    def close(self):
        self._closed = True
        self._cursor.close()
        self._db.close()


class dbopen:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __enter__(self):
        self._db = DBConnection(**self._kwargs)
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()

def _setdbfields():
    with dbopen() as db:
        tables = [i[0] for i in db.execute('SHOW TABLES;')]
        return {table: [i[0] for i in db.execute('SHOW FIELDS FROM {};'.format(table))] for table in tables}


def strdates(dictobject:dict):
    for i in dictobject:
        if isinstance(dictobject[i], datetime.date) or \
                isinstance(dictobject[i], datetime.time) or \
                isinstance(dictobject[i], datetime.datetime):
            dictobject[i] = str(dictobject[i])


class get:
    def __init__(self, db:dbopen):
        self._db = db

    def city(self, city_id:int) -> list:
        return self._db.execute("SELECT * FROM cities WHERE city_id={}".format(city_id), dbfields['cities'])

    def user(self, user_id:int) -> list:
        return self._db.execute("SELECT * FROM users WHERE user_id={}".format(user_id), dbfields['users'])

    def court(self, court_id:int) -> list:
        return self._db.execute("SELECT * FROM courts WHERE court_id={}".format(court_id), dbfields['courts'])

    def game_type(self, type_id:int) -> list:
        return self._db.execute("SELECT * FROM game_types WHERE type_id={}".format(type_id), dbfields['game_types'])

    def game(self, game_id:int) -> list:
        return self._db.execute("SELECT * FROM games WHERE game_id={}".format(game_id), dbfields['games'])

    def sport_type(self, sport_id:int) -> list:
        return self._db.execute("SELECT * FROM sport_types WHERE sport_id={}".format(sport_id), dbfields['sport_types'])


dbfields = _setdbfields()