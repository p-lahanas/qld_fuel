from typing import Any, Callable

import pyodbc
from sqlalchemy import Engine, create_engine


def make_pgsql_connection(connection_string: str, credential: Any) -> pyodbc.Connection:
    return pyodbc.connect(connection_string)


def make_db_engine(
    connection_string: str,
    connection_creator: Callable[[str], pyodbc.Connection] = make_pgsql_connection,
) -> Engine:
    return create_engine(
        "mssql+pyodbc://", creator=lambda: connection_creator(connection_string)
    )
