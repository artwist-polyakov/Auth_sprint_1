import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR
}


class AdminSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='allow')

    logging_level: str = "INFO"

    postgres_host: str = ...
    postgres_port: int = ...
    postgres_name: str = ...
    postgres_user: str = ...
    postgres_password: str = ...

    secret_key: str = ...
    debug: bool = ...

    def get_logging_level(self) -> int:
        return log_levels.get(self.logging_level, logging.INFO)


settings = AdminSettings()

logging.basicConfig(
    level=settings.get_logging_level(),
    format='%(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)
