from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MS SQL DB connection DSN
    SQL_DB_DSN: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),  # , env_file_encoding="utf-8"
    )
