from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
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


class RabbitSettings(BaseSettings):
    """Настройки Rabbit."""

    model_config = SettingsConfigDict(env_prefix="rabbit_mq_")
    host: str
    port: int
    amqp_port: int
    user: str
    password: str


class Settings:
    """Настройки проекта."""

    rabbit: RabbitSettings = RabbitSettings()
    postgres: PostgresSettings = PostgresSettings()

    def get_postgres_dsn(self) -> str:
        return self.postgres.get_dsn()


@lru_cache
def get_settings():
    return Settings()
