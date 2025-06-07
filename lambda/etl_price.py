import json

import fuelpricesqld.api as fa
import fuelpricesqld.etls as etls
from fuelpricesqld.database.session import make_db_engine
from sqlalchemy.orm import Session

from share.lib import Settings, get_api_token


def lambda_handler(event, context):
    api_token = get_api_token()
    api_client = fa.Client(api_token)

    settings = Settings()  # type: ignore

    engine = make_db_engine(settings.PSQL_DB_CONNECTION_STRING)

    with Session(engine) as session:
        etls.etl_prices(session, api_client)
        session.commit()

    return {"statusCode": 200, "body": json.dumps("Data ingestion complete")}
