from typing import get_type_hints

_DECORATED_ATTR = "_sql"


class SQL:
    def joinattr(self, a, b, join_type, select, on):
        def join(where=None):
            sql = f"""
            select {select}
            from {a}
            {join_type} join {b}
            on {on}
            """
            if where:
                sql += f"where {where}"
            return sql

        setattr(self, join.__name__, join)

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

        def select(where=None):
            select = f"select * from {self.name}"
            if where:
                select += f"where {where}"
            return select

        setattr(self, create.__name__, create)
        setattr(self, drop.__name__, drop)
        setattr(self, insert.__name__, insert)
        setattr(self, select.__name__, select)


def sql_table(primary_keys=[]):
    def decorator(_namedtuple):
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

    return decorator


def sql_join(a, b, join_type, on, distinct=False):
    def decorator(_namedtuple):
        if hasattr(_namedtuple, _DECORATED_ATTR):
            _sql = getattr(_namedtuple, _DECORATED_ATTR)
        else:
            _sql = SQL()
            setattr(_namedtuple, _DECORATED_ATTR, _sql)

        select = ", ".join(_namedtuple._fields)
        if distinct:
            select = "distinct " + select

        _sql.joinattr(
            a if isinstance(a, str) else a.__name__.lower(),
            b if isinstance(b, str) else b.__name__.lower(),
            join_type,
            select=select,
            on=on,
        )
        return _namedtuple

    return decorator
