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


class ClickHouseSettings(_BaseSettings):
    """Настройки clickhouse."""

    model_config = SettingsConfigDict(
        env_prefix="clickhouse_", env_file_encoding="utf-8"
    )
    host: str = ...
    port: int = ...
    database: str = ...


class FlaskSettings(_BaseSettings):
    """Настройки Flask."""

    model_config = SettingsConfigDict(env_prefix="flask_")
    port: int


class Settings(CommonSettings):
    """Настройки проекта."""

    kafka: KafkaSettings = KafkaSettings()
    clickhouse: ClickHouseSettings = ClickHouseSettings()
    flask: FlaskSettings = FlaskSettings()


settings = Settings()
