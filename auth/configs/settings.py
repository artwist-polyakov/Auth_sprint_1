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
    project_name: str = "movie_api_default"
    logging_level: str = "INFO"

    redis_host: str = ...
    redis_port: int = 6379

    postgres_host: str = ...
    postgres_port: int = ...
    postgres_name: str = ...
    postgres_user: str = ...
    postgres_password: str = ...

    postgres_schema_2: str = ...

    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 7

    jaeger_host: str = ...
    jaeger_port: int = ...
    jaeger_logs_in_console: bool = False

    yandex_oauth_client_id: str = ...
    yandex_oauth_client_secret: str = ...
    yandex_oauth_url: str = ...

    requests_rate_limit: int = ...

    enable_tracing: bool = ...

    yandex_login_url: str = "https://login.yandex.ru/info"
    yandex_revoke_token_url: str = "https://oauth.yandex.ru/revoke_token"
    yandex_oauth_method_name: str = "yandex"

    sentry_dsn: str = ...
    sentry_enable_tracing: bool = True

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)

    class Config:
        env_file = '.env'


settings = Settings()


class RedisSettings(BaseSettings):
    host: str = settings.redis_host
    port: int = settings.redis_port
    db: int = 0


class RedisCacheSettings(RedisSettings):
    db: int = 0


class RedisLogoutSettings(RedisSettings):
    db: int = 1
    access_lifetime: int = settings.access_token_expire_minutes * 60
    refresh_lifetime: int = settings.refresh_token_expire_minutes * 60


class RedisRateLimitterSettings(RedisSettings):
    db: int = 2
    rate_limit: int = settings.requests_rate_limit


class PostgresSettings(BaseSettings):
    db: str = settings.postgres_name
    user: str = settings.postgres_user
    password: str = settings.postgres_password
    host: str = settings.postgres_host
    port: int = settings.postgres_port


pstg = PostgresSettings()


class PostgresDSN(BaseSettings):
    dsn: str = (f'postgresql+asyncpg://'
                f'{pstg.user}:{pstg.password}@{pstg.host}:'
                f'{pstg.port}/{pstg.db}')


pstg_dsn = PostgresDSN().dsn


@lru_cache
def get_settings():
    return settings
