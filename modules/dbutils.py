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
        if not self._closed:
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


dbfields = _setdbfields()