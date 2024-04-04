from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = ...
    redis_port: int = 6379
    elastic_host: str = ...
    elastic_port: int = 9200
    postgres_host: str = ...
    postgres_port: int = ...
    postgres_name: str = ...
    postgres_user: str = ...
    postgres_password: str = ...

    class Config:
        env_file = ".env"


settings = Settings()


class ElasticDsn(BaseSettings):
    scheme: str = "http"
    host: str = settings.elastic_host
    port: int = settings.elastic_port


class ElasticSettings(BaseSettings):
    hosts: list[ElasticDsn] = [ElasticDsn()]
    timeout: int = 60
    max_retries: int = 10
    retry_on_timeout: bool = True


class PostgresSettings(BaseSettings):
    dbname: str = settings.postgres_name
    user: str = settings.postgres_user
    password: str = settings.postgres_password
    host: str = settings.postgres_host
    port: int = settings.postgres_port
