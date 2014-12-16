import pymysql

import config


default_connection = {
    'host': config.db.dbhost,
    'user': config.db.dbuser,
    'passwd': config.db.dbpasswd,
    'db': config.db.dbname,
    'charset': 'utf8'
}

logsdb_connection = {
    'host': config.logs.dbhost,
    'user': config.logs.dbuser,
    'passwd': config.logs.dbpasswd,
    'db': config.logs.dbname,
    'charset': 'utf8'
}


class DatabaseError(Exception):
    def __init__(self, e:Exception, query:str):
        super().__init__(query, *e.args)


class DBConnection:
    def __init__(self, **kwargs):
        if len(kwargs) == 0:
            self._db = pymysql.connect(**default_connection)
            self._connection_kwargs = default_connection
        else:
            self._db = pymysql.connect(**kwargs)
            self._connection_kwargs = kwargs
        self._closed = False
        self._locked = False
        self._cursor = self._db.cursor()
        self._last = None

    def _execute(self, query:str):
        try:
            return self._cursor.execute(query)
        except Exception as e:
            raise DatabaseError(e, query)

    def execute(self, query:str, mapnames:list=None) -> list:
        """
        Execute a SQL query
        :param query: SQL query
        :param mapnames: field names
        :return:  list of lines, where line is also a list of ordered database fields
        """
        if self.closed:
            self.reconnect()
        if self._execute(query) == 0:
            self._last = list()
        else:
            data = self._cursor.fetchall()
            # люблю питон за такие моменты
            self._last = [dict(zip(mapnames, list(line))) if mapnames else list(line) for line in
                          data] if data else list()
        return self._last

    def execute_sql_query(self, sql:SqlQuery) -> list:
        pass

    def last(self) -> list:
        return self._last

    def reconnect(self):
        if not self.closed:
            self.close()
        self._db = pymysql.connect(**self._connection_kwargs)
        self._cursor = self._db.cursor()
        self._closed = False

    def lock(self, table:str, method:str='WRITE'):
        if self._locked:
            raise RuntimeError("Trying to lock locked connection")
        self.execute("LOCK TABLES {} {}".format(table, method))
        self._locked = True

    def unlock(self):
        if not self._locked:
            raise RuntimeError("Trying to unlock unlocked connection")
        self.execute("UNLOCK TABLES")
        self._locked = False

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


def setdbfields(kwargs=default_connection):
    with dbopen(**kwargs) as db:
        tables = [i[0] for i in db.execute('SHOW TABLES;')]
        return {table: [i[0] for i in db.execute('SHOW FIELDS FROM {};'.format(table))] for table in tables}


dbfields = setdbfields()


class SqlQuery:
    def __init__(self, statement:str, table_name:str):
        self._statement = statement
        self._table_name = table_name
        self._fields = '*'
        self._where = list()

    def set_fields(self, fields:list):
        self._fields = fields

    def add_where_and(self, value:str):
        self._where.append(('AND', value))

    def add_where_or(self, value:str):
        self._where.append(('OR', value))

    def add_where(self, value:str):
        self._where.append((None, value))

    def __str__(self):
        pass

class sql:
    @staticmethod
    def select(table_name:str):
        return

    @staticmethod
    def insert(table_name:str):
        pass

    @staticmethod
    def delete(table_name:str):
        pass

    @staticmethod
    def update(table_name:str):
        pass