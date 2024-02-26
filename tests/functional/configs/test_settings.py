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

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)


settings = TestSettings()

logging.basicConfig(
    level=settings.get_logging_level(),
    format='%(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)
