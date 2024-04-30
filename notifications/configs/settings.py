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

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)

    class Config:
        env_file = '.env'


settings = Settings()


@lru_cache
def get_settings():
    return settings
