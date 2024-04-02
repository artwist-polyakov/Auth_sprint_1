import os

# Применяем настройки логирования

# Настройки Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))

# Настройки Elasticsearch
ELASTIC_HOST = os.environ.get("ELASTIC_HOST")
ELASTIC_PORT = int(os.environ.get("ELASTIC_PORT"))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Postgres DSL
DSL = {
    "dbname": os.environ.get("POSTGRES_NAME"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT"),
}

SQLITE_PATH = os.environ.get("SQLITE_PATH")
