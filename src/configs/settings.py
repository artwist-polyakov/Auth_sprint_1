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
    elastic_host: str = ...
    elastic_port: int = 9200

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)

    class Config:
        env_file = '.env'


settings = Settings()


class RedisSettings(BaseSettings):
    host: str = settings.redis_host
    port: int = settings.redis_port


class ElasticDsn(BaseSettings):
    scheme: str = 'http'
    host: str = settings.elastic_host
    port: int = settings.elastic_port


class ElasticSettings(BaseSettings):
    hosts: list[ElasticDsn] = [ElasticDsn()]
    timeout: int = 60
    max_retries: int = 10
    retry_on_timeout: bool = True
