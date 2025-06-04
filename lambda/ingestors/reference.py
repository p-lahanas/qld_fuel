import json
import os
import uuid
from datetime import datetime

import boto3
import fuelpricesqld.api as fa
from fuelpricesqld.lib import get_api_token


def create_reference_object(name: str) -> str:
    date_path = datetime.now().strftime("%Y/%m/%d")
    file_name = f"{uuid.uuid4()}.json"

    return f"reference/{name}/{date_path}/{file_name}"


def lambda_handler(event, context):
    api_token = get_api_token()
    api_session = fa.Client(api_token)

    fuel_types = json.dumps(api_session.get_fuel_types(fa.COUNTRY_ID_AUS))
    fuel_brands = json.dumps(api_session.get_country_brands(fa.COUNTRY_ID_AUS))
    regions = json.dumps(api_session.get_country_geographic_regions(fa.COUNTRY_ID_AUS))

    # Just store BNE sites for now
    site_details = json.dumps(
        api_session.get_full_site_details(
            fa.COUNTRY_ID_AUS, fa.REGION_LEVEL_BNE, fa.REGION_ID_BNE
        )
    )

    # Upload our data to s3
    client = boto3.client("s3")
    bucket = os.environ["S3Bucket"]

    client.put_object(
        Body=fuel_brands, Bucket=bucket, Key=create_reference_object("brands")
    )
    client.put_object(
        Body=fuel_types, Bucket=bucket, Key=create_reference_object("fueltypes")
    )
    client.put_object(
        Body=regions, Bucket=bucket, Key=create_reference_object("regions")
    )
    client.put_object(
        Body=site_details, Bucket=bucket, Key=create_reference_object("sitedetails")
    )

    return {"statusCode": 200, "body": json.dumps("Data ingestion complete")}
