from typing import Any

from core.settings import get_settings
from pymongo import MongoClient


class MongoService:

    def __init__(self):
        self.client = MongoClient(get_settings().mongo.host, get_settings().mongo.port)
        self.db = self.client[get_settings().mongo.database]

    def data_recording(
            self,
            data: list[dict],
            collection_name: str,
            batch_size: int = None
    ) -> Any:
        result_ids = []
        collection = self.db[collection_name]
        if batch_size is None:
            batch_size = len(data)
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            res = collection.insert_many(batch)
            result_ids.extend(res.inserted_ids)
        return result_ids

    def data_reading(
            self,
            condition: dict,
            collection_name: str,
            multiple: bool = False
    ) -> Any:
        collection = self.db[collection_name]
        if multiple:
            results = [item for item in collection.find(condition)]
            return results
        return collection.find_one(condition)

    def __enter__(self):
        # Возвращает объект, который будет использоваться в контекстном блоке.
        # В данном случае возвращаем self, так как сам объект позволяет работу с Mongo.
        return self

    def __exit__(self, exc_type, exc_value, traceback):
         # Закрываем соединение с MongoDB при выходе из контекстного блока.
         self.client.close()