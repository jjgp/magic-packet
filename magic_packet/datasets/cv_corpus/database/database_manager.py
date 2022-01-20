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

    def create(self, *records):
        for record in records:
            self._cur.execute(record._sql_create())

    def drop(self, *records):
        for record in records:
            self._cur.execute(record._sql_drop())

    def insert(self, record):
        self._cur.execute(record._sql_insert(), record)

    def insertmany(self, records):
        self._cur.executemany(records[0]._sql_insert(), records)
