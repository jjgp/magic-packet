import os
import sqlite3 as sql


class DatabaseManager:
    def __init__(self, database):
        self._database = os.path.abspath(database)

    def __enter__(self):
        self._conn = sql.connect(self._database)
        self._cur = self._conn.cursor()
        return self

    def __exit__(self, *_):
        self._cur.close()
        self._conn.close()

    def commit(self):
        self._conn.commit()

    def execute(self, sql, parameters=()):
        self._cur.execute(sql, parameters)

    def executemany(self, sql, seq_of_parameters):
        self._cur.executemany(sql, seq_of_parameters)

    def fetchall(self):
        return self._cur.fetchall()

    def create(self, *records):
        for record in records:
            self._cur.execute(record._sql.create())

    def drop(self, *records):
        for record in records:
            self._cur.execute(record._sql.drop())

    def insert(self, record):
        self._cur.execute(record._sql.insert(), record)

    def insertmany(self, records):
        self._cur.executemany(records[0]._sql.insert(), records)

    def join(self, record, where=None, parameters=None):
        return self._query(record, record._sql.join, where, parameters)

    def select(self, record, where=None, parameters=None):
        return self._query(record, record._sql.select, where, parameters)

    def update(self, record, where):
        self._cur.execute(record._sql.update(where), record)

    def _query(self, record, fn, where, parameters):
        self._cur.execute(fn(where), parameters)
        return map(record._make, self._cur.fetchall())
