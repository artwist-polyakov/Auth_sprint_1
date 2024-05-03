from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class _BaseSettings(BaseSettings):
    """Базовые настройки."""

    base_dir: Path = Path(__file__).parent.parent.resolve()
    model_config = SettingsConfigDict(
        env_file=str(base_dir / "../../.env"), extra="ignore"
    )


class CommonSettings(_BaseSettings):
    """Общие настройки, не относящиеся к коду."""

    project_name: str


class PostgresSettings(_BaseSettings):
    """Настройки Postgres."""

    model_config = SettingsConfigDict(env_prefix="notifications_db_")

    host: str
    port: int
    name: str
    user: str
    password: str

    def get_dsn(self) -> str:
        return (f"postgresql://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}")


class RabbitSettings(_BaseSettings):
    """Настройки Rabbit."""

    model_config = SettingsConfigDict(env_prefix="rabbit_mq_")
    host: str
    port: int
    amqp_port: int
    user: str
    password: str


class Settings(CommonSettings):
    """Настройки проекта."""

    rabbit: RabbitSettings = RabbitSettings()
    postgres: PostgresSettings = PostgresSettings()


@lru_cache
def get_settings():
    return Settings()
