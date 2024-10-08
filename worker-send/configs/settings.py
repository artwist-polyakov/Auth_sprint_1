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


class MailSettings(BaseSettings):
    """Настройки почты."""

    model_config = SettingsConfigDict(env_prefix="mail_")
    smtp_server: str
    smtp_port: int
    login: str
    password: str
    domain: str


class WebsocketSettings(BaseSettings):
    """Настройки websocket."""

    model_config = SettingsConfigDict(env_prefix="websocket_")
    host: str
    port: int


class Settings:
    """Настройки проекта."""

    rabbit: RabbitSettings = RabbitSettings()
    postgres: PostgresSettings = PostgresSettings()
    mail: MailSettings = MailSettings()
    websocket: WebsocketSettings = WebsocketSettings()

    def get_postgres_dsn(self) -> str:
        return self.postgres.get_dsn()

    def get_rabbit_settings(self) -> RabbitSettings:
        return self.rabbit

    def get_mail_settings(self) -> MailSettings:
        return self.mail

    def get_websocket_settings(self) -> WebsocketSettings:
        return self.websocket


@lru_cache
def get_settings():
    return Settings()
