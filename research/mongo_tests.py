import time
from typing import Any

from pymongo import MongoClient

from pymongo.collection import Collection

# Создание клиента
client = MongoClient('localhost', 27017)

# Подключение к базе данных
db = client['TestDB']


def insert_document(*, data: list[dict], collection: Collection = db.users) -> Any:
    result_ids = []
    start = time.monotonic()
    for doc in data:
        res = collection.insert_one(doc)
        result_ids.append(res.inserted_id)
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
