import logging

from pydantic_settings import BaseSettings

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR
}


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


class PostgresSettings(BaseSettings):
    db: str = settings.postgres_name
    user: str = settings.postgres_user
    password: str = settings.postgres_password
    host: str = settings.postgres_host
    port: int = settings.postgres_port