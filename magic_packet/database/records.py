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
        n_cols = len(columns)
        insert_values_sql = ", ".join(["?"] * n_cols)
        schema = ", ".join(f"{c} {a}" for c, a in zip(columns, annotations))
        if primary_keys:
            schema += f", primary key ({', '.join(primary_keys)})"

        def create():
            return f"create table {name} ({schema})"

        def drop():
            return f"drop table if exists {name}"

        def insert():
            return f"insert into {name} values ({insert_values_sql})"

        def select(where=None):
            select = f"select * from {name}"
            if where:
                select += f" where {where}"
            return select

        setattr(self, create.__name__, create)
        setattr(self, drop.__name__, drop)
        setattr(self, insert.__name__, insert)
        setattr(self, select.__name__, select)

        self.updateattr(name, columns)

    def updateattr(self, name, columns):
        set_sql = ", ".join(f"{column}=:{column}" for column in columns)

        def update(where):
            update = f"""
            update {name}
            set {set_sql}
            """
            if where:
                update += where
            return where

        setattr(self, update.__name__, update)


def sql_table(primary_keys=[]):
    def decorator(_namedtuple):
        implemented_annotations = {float: "real", int: "integer", str: "varchar"}
        table_name = _namedtuple.__name__.lower()

        columns, annotations = [], []
        for name, t in get_type_hints(_namedtuple).items():
            if t not in implemented_annotations:
                raise NotImplementedError(f"The type {t} is not implemented")
            columns.append(name)
            annotations.append(implemented_annotations[t])

        _sql = _check_decorated_attr(_namedtuple)
        _sql.tableattr(table_name, columns, annotations, primary_keys)
        return _namedtuple

    return decorator


def sql_join(a, b, join_type, on, distinct=False):
    def decorator(_namedtuple):
        select = ", ".join(_namedtuple._fields)
        if distinct:
            select = "distinct " + select

        _sql = _check_decorated_attr(_namedtuple)
        _sql.joinattr(
            a if isinstance(a, str) else a.__name__.lower(),
            b if isinstance(b, str) else b.__name__.lower(),
            join_type,
            select=select,
            on=on,
        )
        return _namedtuple

    return decorator


def sql_update(table):
    def decorater(_namedtuple):
        columns = [field for field in _namedtuple._fields]
        _sql = _check_decorated_attr(_namedtuple)
        _sql.updateattr(
            table if isinstance(table, str) else table.__name__.lower(), columns
        )
        return _namedtuple

    return decorater


def _check_decorated_attr(obj):
    if hasattr(obj, _DECORATED_ATTR):
        _sql = getattr(obj, _DECORATED_ATTR)
    else:
        _sql = SQL()
        setattr(obj, _DECORATED_ATTR, _sql)
    return _sql
