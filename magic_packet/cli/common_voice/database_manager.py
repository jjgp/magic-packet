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
        if self._conn.in_transaction:
            self._conn.commit()
        self._conn.close()

    def __getattr__(self, name):
        return getattr(self._cur, name)
