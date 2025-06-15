import fuelpricesqld.api as fa
import fuelpricesqld.etls as etls
from fuelpricesqld.database.session import make_db_engine
from sqlalchemy.orm import Session

from app import Settings


def etl():
    settings = Settings()  # type: ignore

    # Create fuelpricesqld api client
    api_token = settings.FUEL_PRICES_QLD_API_TOKEN
    api_client = fa.Client(api_token)

    # Connect to DB
    db_connection_string = settings.PSQL_DB_CONNECTION_STRING
    engine = make_db_engine(db_connection_string)

    with Session(engine) as session:
        # Order of these does matter due to foreign key constraints
        # Put sites after brands & ensure countries table is seeded
        etls.etl_brands(session, api_client)
        etls.etl_fuels(session, api_client)
        etls.etl_regions(session, api_client)
        etls.etl_sites(session, api_client)

        session.commit()


if __name__ == "__main__":
    etl()
