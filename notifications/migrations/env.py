import os
from logging.config import fileConfig

from alembic import context
from db.models.base import Base
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# from db.models.notifications import Notifications
# from db.models.tasks import Tasks

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

load_dotenv("../.env")


def get_alchemy_url() -> str:
    user = os.getenv("NOTIFICATIONS_DB_USER")
    password = os.getenv("NOTIFICATIONS_DB_PASSWORD")
    host = os.getenv("NOTIFICATIONS_DB_HOST")
    port = os.getenv("NOTIFICATIONS_DB_PORT")
    name = os.getenv("NOTIFICATIONS_DB_NAME")
    # return f'postgresql+asyncpg://{user}:{password}@localhost:{port}/{name}?async_fallback=True'
    return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}?async_fallback=True'


config.set_main_option(name='sqlalchemy.url', value=get_alchemy_url())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()