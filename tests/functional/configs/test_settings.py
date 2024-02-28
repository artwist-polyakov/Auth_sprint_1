import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR
}


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='allow')

    logging_level: str = "INFO"
    redis_host: str = ...
    redis_port: int = ...
    es_1_host: str = ...
    es_2_host: str = ...
    elastic_port: int = ...

    movies_url: str = ...
    auth_url: str = ...

    postgres_host: str = ...
    postgres_port: int = ...
    postgres_name: str = ...
    postgres_user: str = ...
    postgres_password: str = ...

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)


settings = TestSettings()

logging.basicConfig(
    level=settings.get_logging_level(),
    format='%(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


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
