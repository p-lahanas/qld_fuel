import boto3

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MS SQL DB connection DSN
    PSQL_DB_CONNECTION_STRING: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),  # , env_file_encoding="utf-8"
    )


def get_api_token() -> str:
    client = boto3.client("ssm")
    response = client.get_parameter(Name="qld_fuel_token", WithDecryption=True)

    return response["Parameter"]["Value"]
