from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Finds the backend directory regardless of the directory used to start the application.
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str                  # Database connection URL loaded from environment variables
    secret_key: str                    # Secret key used for secure authentication
    access_token_expire_minutes: int = 60  # Sets tokens to expire after 60 minutes by default

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",    # Loads local development configuration from the backend .env file
        env_file_encoding="utf-8",
    )


settings = Settings()                  # Creates the settings object for use throughout the application