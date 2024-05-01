import logging
from functools import lru_cache

from core.logging_setup import setup_root_logger
from pydantic_settings import BaseSettings

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR
}

setup_root_logger()


class Settings(BaseSettings):
    api_name: str = "Notifications API"
    logging_level: str = "INFO"

    jaeger_host: str = ...
    jaeger_port: int = ...
    jaeger_logs_in_console: bool = False

    enable_tracing: bool = ...

    sentry_dsn: str = ...
    sentry_enable_tracing: bool = True

    notifications_db_host: str = ...
    notifications_db_port: int = ...
    notifications_db_name: str = ...
    notifications_db_user: str = ...
    notifications_db_password: str = ...

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)

    class Config:
        env_file = '.env'


settings = Settings()


class PostgresDSN(BaseSettings):
    host: str = settings.notifications_db_host
    port: int = settings.notifications_db_port
    db: str = settings.notifications_db_name
    user: str = settings.notifications_db_user
    password: str = settings.notifications_db_password

    def get_dsn(self) -> str:
        return (f"postgresql+asyncpg://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.db}")


@lru_cache
def get_postgres_dsn():
    return PostgresDSN().get_dsn()


@lru_cache
def get_settings():
    return settings
