from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "NotesContacts"
    database_url: str = Field(
        "postgresql://postgres:postgres@localhost:5432/notes_contacts",
        env="DATABASE_URL",
    )
    db_pool_size: int = Field(2, env="DB_POOL_SIZE")
    max_limit: int = Field(0, env="MAX_LIMIT")  # zero disables server side caps
    log_pii: bool = Field(True, env="LOG_PII")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
