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

    elastic_host: str = ...
    elastic_port: int = 9200

    postgres_host: str = ...
    postgres_port: int = ...
    postgres_name: str = ...
    postgres_user: str = ...
    postgres_password: str = ...

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


class RedisSettings(BaseSettings):
    host: str = settings.redis_host
    port: int = settings.redis_port
    db: int = 0


class RedisCacheSettings(RedisSettings):
    db: int = 0


class ElasticDsn(BaseSettings):
    scheme: str = 'http'
    host: str = settings.elastic_host
    port: int = settings.elastic_port


class ElasticSettings(BaseSettings):
    hosts: list[ElasticDsn] = [ElasticDsn()]
    timeout: int = 60
    max_retries: int = 10
    retry_on_timeout: bool = True


class PostgresSettings(BaseSettings):
    db: str = settings.postgres_name
    user: str = settings.postgres_user
    password: str = settings.postgres_password
    host: str = settings.postgres_host
    port: int = settings.postgres_port


class JWTSecuritySettings(BaseSettings):
    jwt_cookie_csrf_protect: bool = False
    openssl_key: str = ...
    algorithm: str = 'HS256'
    internal_secret_token: str = ...

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return settings
