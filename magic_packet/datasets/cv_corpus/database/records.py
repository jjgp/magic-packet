from typing import NamedTuple, get_type_hints

_DECORATED_ATTR = "_sql"


class SQL:
    def inner_joinattr(self, a, b, select, on):
        def inner_join(where=None):
            sql = f"""
            select {select}
            from {a}
            inner join {b}
            on {on}
            """
            if where:
                sql += f"where {where}"
            return sql

        setattr(self, inner_join.__name__, inner_join)

    def tableattr(self, name, columns, annotations, primary_keys):
        self.n_cols = len(columns)
        self.name = name
        schema = ", ".join(f"{c} {a}" for c, a in zip(columns, annotations))
        if primary_keys:
            schema += f", primary key ({', '.join(primary_keys)})"
        self.schema = schema

        def create():
            return f"create table {self.name} ({self.schema})"

        def drop():
            return f"drop table if exists {self.name}"

        def insert():
            return f"insert into {self.name} values ({', '.join(['?'] * self.n_cols)})"

        setattr(self, create.__name__, create)
        setattr(self, drop.__name__, drop)
        setattr(self, insert.__name__, insert)


def sql_table(primary_keys=[]):
    def _namedtuple_decorator(_namedtuple):
        implemented_annotations = {int: "integer", str: "varchar"}
        table_name = _namedtuple.__name__.lower()

        columns, annotations = [], []
        for name, t in get_type_hints(_namedtuple).items():
            if t not in implemented_annotations:
                raise NotImplementedError(f"The type {t} is not implemented")
            columns.append(name)
            annotations.append(implemented_annotations[t])

        if hasattr(_namedtuple, _DECORATED_ATTR):
            _sql = getattr(_namedtuple, _DECORATED_ATTR)
        else:
            _sql = SQL()
            setattr(_namedtuple, _DECORATED_ATTR, _sql)

        _sql.tableattr(table_name, columns, annotations, primary_keys)
        return _namedtuple

    return _namedtuple_decorator


def sql_inner_join(record_a, record_b, on):
    def _namedtuple_decorator(_namedtuple):
        if hasattr(_namedtuple, _DECORATED_ATTR):
            _sql = getattr(_namedtuple, _DECORATED_ATTR)
        else:
            _sql = SQL()
            setattr(_namedtuple, _DECORATED_ATTR, _sql)

        _sql.inner_joinattr(
            record_a.__name__.lower(),
            record_b.__name__.lower(),
            select=", ".join(_namedtuple._fields),
            on=on,
        )
        return _namedtuple

    return _namedtuple_decorator


@sql_table(primary_keys=["id"])
class Clips(NamedTuple):
    id: int
    fname: str
    split: str


@sql_table(primary_keys=["clip_id", "loc"])
class Words(NamedTuple):
    clip_id: int
    loc: int
    word: str


@sql_inner_join(Words, Clips, on="clip_id = id")
class WordsOnClips(NamedTuple):
    clip_id: int
    fname: str
    loc: int
    word: str
    split: str
