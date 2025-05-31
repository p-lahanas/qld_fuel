import logging

import polars as pl
from sqlalchemy.orm import Session

from fuelpricesqld.api import Client
from fuelpricesqld.database.session import make_db_engine
from fuelpricesqld.settings import Settings

from .lib import get_api_token

logger = logging.getLogger(__name__)


def reference_data_etl(session: Session):
    # Load data from the api
    api_client = Client(get_api_token())


def price_data_etl(session: Session):
    pass


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
    )

    settings = Settings()  # type: ignore

    engine = make_db_engine(settings.PSQL_DB_CONNECTION_STRING)

    with Session(engine) as session:
        reference_data_etl(session)
        session.commit()
