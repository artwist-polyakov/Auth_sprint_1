from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    notifications_db_host: str = ...
    notifications_db_port: int = ...
    notifications_db_name: str = ...
    notifications_db_user: str = ...
    notifications_db_password: str = ...

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()


class PostgresDSN(BaseSettings):
    host: str = get_settings().notifications_db_host
    port: int = get_settings().notifications_db_port
    db: str = get_settings().notifications_db_name
    user: str = get_settings().notifications_db_user
    password: str = get_settings().notifications_db_password

    def get_dsn(self) -> str:
        return (f"postgresql://notifications_user:{self.password}"
                f"@{self.host}:{self.port}/{self.db}")


@lru_cache
def get_postgres_dsn():
    return PostgresDSN().get_dsn()
