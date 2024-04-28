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


class RabbitSettings(_BaseSettings):
    """Настройки Rabbit."""

    model_config = SettingsConfigDict(env_prefix="rabbit_")
    host: str
    port: int


class Settings(CommonSettings):
    """Настройки проекта."""

    rabbit: RabbitSettings = RabbitSettings()


settings = Settings()
