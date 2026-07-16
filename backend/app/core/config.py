from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Football IQ AI"
    app_version: str = "0.1.3"
    app_env: str = "development"
    log_level: str = "INFO"
    postgres_db: str = "football_iq_ai"
    postgres_user: str = "athena"
    postgres_password: str = "change_me"
    postgres_host: str = "db"
    postgres_port: int = 5432
    api_football_base_url: str = "https://v3.football.api-sports.io"
    api_football_key: str = Field(default="", repr=False)
    api_football_timeout_seconds: float = 30.0
    api_football_max_retries: int = 3
    knowledge_builder_default_season: int = 2025
    knowledge_builder_delay_seconds: float = 1.2
    knowledge_builder_stop_on_error: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def api_football_is_configured(self) -> bool:
        return bool(self.api_football_key and self.api_football_key != "replace_with_your_api_key")

@lru_cache
def get_settings() -> Settings:
    return Settings()
