from typing import NamedTuple, get_type_hints

from database_manager import DatabaseManager


def SQLTable(primary_keys=[]):
    def _decorator(_namedtuple):
        annotations = {int: "integer", str: "varchar"}
        table = _namedtuple.__name__.lower()

        def _iter_type_hints_schema():
            for name, t in get_type_hints(_namedtuple).items():
                if t not in annotations:
                    raise NotImplementedError(f"The type {t} is not implemented")
                yield f"{name} {annotations[t]}"

        def _sql_create():
            schema = ", ".join(_iter_type_hints_schema())
            if primary_keys:
                schema += f", primary key ({', '.join(primary_keys)})"

            return f"create table {table} ({schema})"

        def _sql_drop():
            return f"drop table if exists {table}"

        def _sql_insert(self):
            values_sql = ", ".join(["?"] * len(self._fields))
            return f"insert into {table} values ({values_sql})"

        setattr(_namedtuple, _sql_create.__name__, _sql_create)
        setattr(_namedtuple, _sql_drop.__name__, _sql_drop)
        setattr(_namedtuple, _sql_insert.__name__, _sql_insert)
        return _namedtuple

    return _decorator


@SQLTable(primary_keys=["id"])
class Clips(NamedTuple):
    id: int
    fname: str
    split: str


@SQLTable(primary_keys=["clip_id", "loc"])
class Words(NamedTuple):
    clip_id: int
    loc: int
    word: str


def SQLInnerJoin(a, b, on):
    def _decorator(_namedtuple):
        def _sql_join(where):
            sql = f"""
            select {", ".join(_namedtuple._fields)}
            from {a.__name__.lower()}
            inner join {b.__name__.lower()}
            on {on}
            """
            if where:
                sql += f"where {where}"
            return sql

        setattr(_namedtuple, _sql_join.__name__, _sql_join)
        return _namedtuple

    return _decorator


@SQLInnerJoin(Words, Clips, on="clip_id = id")
class WordsOnClips(NamedTuple):
    clip_id: int
    fname: str
    loc: int
    word: str
    split: str


if __name__ == "__main__":
    database = "./data/cv-corpus-7.0-2021-07-21/en/index.db"
    with DatabaseManager(database) as db_manager:
        result = db_manager.join(WordsOnClips, where="word = 'fox'")
        print(result)
