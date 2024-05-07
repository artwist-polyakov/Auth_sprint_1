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
    tasks_queue: str
    enriched_queue: str
    notifications_queue: str
    to_sending_queue: str
    tasks_key: str
    enriched_key: str
    notifications_key: str
    to_sending_key: str
    exchange: str


class Settings:
    """Настройки проекта."""

    rabbit: RabbitSettings = RabbitSettings()
    postgres: PostgresSettings = PostgresSettings()

    def get_postgres_dsn(self) -> str:
        return self.postgres.get_dsn()

    def get_rabbit_settings(self) -> RabbitSettings:
        return self.rabbit


@lru_cache
def get_settings():
    return Settings()
