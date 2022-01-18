import os
import sqlite3 as sql


class DatabaseManager(object):
    def __init__(self, database):
        self._database = os.path.abspath(database)

    def __enter__(self):
        self._conn = sql.connect(self._database)
        self._cur = self._conn.cursor()
        return self

    def __exit__(self, *_):
        self._cur.close()
        self._conn.close()


if __name__ == "__main__":
    with DatabaseManager("cv.db") as db_manager:
        pass
