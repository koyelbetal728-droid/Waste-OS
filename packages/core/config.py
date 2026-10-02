"""Central environment-driven configuration for all WasteOS services."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    debug: bool = True
    database_url: str = "postgresql+psycopg2://wasteos:wasteos@localhost:5432/wasteos"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
