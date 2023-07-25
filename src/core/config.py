import os
from typing import Any

from logging import config as logging_config
from pydantic import BaseSettings, PostgresDsn, validator

from src.core.logger import LOGGING


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {'postgres+asyncpg', 'postgresql+asyncpg'}


class Settings(BaseSettings):
    PROJECT_NAME: str = 'FileApp'
    UPLOAD_FOLDER: str = 'download'
    TEST_UPLOAD_FOLDER: str = 'test_download'

    MAX_FILE_SIZE: int = 10 * 1024 * 1024

    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8080

    JWT_SECRET: str
    JWT_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int
    REDIS_PASSWORD: str

    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_MAX_OVERFLOW: int = 20
    POSTGRES_POOL_TIMEOUT: int = 60
    POSTGRES_POOL_RECYCLE: int = 3600

    POSTGRES_DB: str = 'url_app'
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TEST_POSTGRES_DB: str = 'test_url_app'
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    POSTGRES_DSN: str

    SQLALCHEMY_DATABASE_URI: AsyncPostgresDsn | None = None
    TEST_SQLALCHEMY_DATABASE_URI: AsyncPostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", allow_reuse=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:  # noqa B902
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("TEST_SQLALCHEMY_DATABASE_URI", allow_reuse=True)
    def assemble_test_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:  # noqa B902
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("TEST_POSTGRES_USER"),
            password=values.get("TEST_POSTGRES_PASSWORD"),
            host=values.get("TEST_POSTGRES_SERVER"),
            path=f"/{values.get('TEST_POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = '.env.config'
        env_file_encoding = 'utf-8'


settings = Settings()
