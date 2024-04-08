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


class KafkaSettings(_BaseSettings):
    """Настройки kafka."""

    model_config = SettingsConfigDict(env_prefix="kafka_")
    host: str
    port_ui: int
    port: int


class PostgresSettings(_BaseSettings):
    """Настройки postgresql."""
    model_config = SettingsConfigDict(env_prefix="postgres_")
    name: str
    user: str
    password: str
    host: str
    port: int


class Settings(CommonSettings):
    """Настройки проекта."""

    kafka: KafkaSettings = KafkaSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()


class PostgresDSN(BaseSettings):
    dsn: str = (f'postgresql+asyncpg://'
                f'{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:'
                f'{settings.postgres.port}/{settings.postgres.name}')


pstg_dsn = PostgresDSN().dsn
