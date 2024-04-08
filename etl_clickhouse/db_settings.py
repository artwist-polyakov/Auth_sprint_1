from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class _BaseSettings(BaseSettings):
    """Базовые настройки."""

    base_dir: Path = Path(__file__).parent.resolve()
    model_config = SettingsConfigDict(
        env_file=str(base_dir / "../.env"), extra="ignore"
    )


class CommonSettings(_BaseSettings):
    """Общие настройки, не относящиеся к коду."""

    project_name: str


class PostgresSettings(_BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_", env_file_encoding="utf-8")
    db: str = ...
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...


class ClickHouseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="clickhouse_", env_file_encoding="utf-8"
    )
    host: str = ...
    port: int = ...
    database: str = ...


class Settings(CommonSettings):
    """Настройки проекта."""

    clickhouse: ClickHouseSettings = ClickHouseSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
