from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MS SQL DB connection DSN
    PSQL_DB_CONNECTION_STRING: str
    FUEL_PRICES_QLD_API_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),  # , env_file_encoding="utf-8"
    )
