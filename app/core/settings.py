from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # Base class for settings, allowing values to be overridden by environment variables.
    api_version: str = "0.0.1"

    db_uri: str = "postgresql+asyncpg://admin:1234@postgres:5432/carekeeper"  # config("DATABASE_URL")

    secret_key: str = config("SECRET_KEY")
    algorithm: str = config("ALGORITHM")
    expire_minutes: int = config("JWT_EXPIRE_MINUTES")


settings = Settings()
