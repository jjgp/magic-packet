import os
import sqlite3 as sql


class Table:
    name = ""
    column_schema = []

    def create_sql(self):
        column_schema = ", ".join(self.column_schema)
        return f"create table {self.name} ({column_schema})"

    def drop_sql(self):
        return f"drop table if exists {self.name}"

    def insert_sql(self):
        values_sql = ", ".join(["?" for _ in range(len(self.column_schema))])
        return f"insert into {self.name} values ({values_sql})"


class WordsTable(Table):
    name = "words"
    column_schema = ["clip_id integer", "loc integer", "word integer"]


class ClipsTable(Table):
    name = "clips"
    column_schema = ["id integer primary key", "split varchar", "name vachar"]


class DatabaseConfig:
    def __init__(self, tables=[WordsTable(), ClipsTable()]):
        self.tables = {table.name: table for table in tables}


class DatabaseManager(object):
    def __init__(self, database, config=DatabaseConfig()):
        self._config = config
        self._database = os.path.abspath(database)

    def __enter__(self):
        self._conn = sql.connect(self._database)
        self._cur = self._conn.cursor()
        return self

    def __exit__(self, *_):
        self._cur.close()
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        for table in self._config.tables.values():
            self._cur.execute(table.create_sql())

    def drop_tables(self):
        for table in self._config.tables.values():
            self._cur.execute(table.drop_sql())

    def insert(self, table_name, parameters):
        self._cur.execute(self._config.tables[table_name].insert_sql(), parameters)

    def insert_many(self, table_name, *parameters):
        self._cur.executemany(self._config.tables[table_name].insert_sql(), *parameters)
