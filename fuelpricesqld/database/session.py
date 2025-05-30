from sqlalchemy import Engine, create_engine


def make_db_engine(
    connection_string: str,
) -> Engine:
    return create_engine(connection_string, plugins=["geoalchemy2"])
