import json
import os
import uuid
from datetime import datetime

import boto3
import fuelpricesqld.api as fa

from share.lib import get_api_token


def create_price_object() -> str:
    dt_now = datetime.now()
    date_path = dt_now.strftime("%Y/%m/%d/%H")
    file_name = f"{dt_now.strftime('%H:%M')}_{uuid.uuid4()}.json"

    return f"prices/{date_path}/{file_name}"


def lambda_handler(event, context):
    api_token = get_api_token()
    api_session = fa.Client(api_token)

    fuel_prices = json.dumps(
        api_session.get_sites_prices(
            fa.COUNTRY_ID_AUS, fa.REGION_LEVEL_BNE, fa.REGION_ID_BNE
        )
    )

    # Upload our data to s3
    client = boto3.client("s3")
    bucket = os.environ["S3Bucket"]

    client.put_object(Body=fuel_prices, Bucket=bucket, Key=create_price_object())

    return {"statusCode": 200, "body": json.dumps("Data ingestion complete")}
