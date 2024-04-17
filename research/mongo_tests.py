import time
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection

# Создание клиента
client = MongoClient('localhost', 27017)

# Подключение к базе данных
db = client['TestDB']


def insert_documents_in_batches(*, data: list[dict], batch_size: int, collection: Collection = db.users) -> Any:
    result_ids = []
    start = time.monotonic()
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        res = collection.insert_many(batch)
        result_ids.extend(res.inserted_ids)
    end = time.monotonic()
    return result_ids, end - start


def find_data(*, condition: dict, collection: Collection = db.users, multiple: bool = False):
    start = time.monotonic()
    if multiple:
        results = [item for item in collection.find(condition)]
        end = time.monotonic()
        return results, end - start
    end = time.monotonic()
    return collection.find_one(condition), end - start
