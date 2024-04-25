import json
from functools import lru_cache
from typing import Any

from core.settings import settings
from pymongo import MongoClient
from bson import json_util


class MongoService:

    def __init__(self):
        self.client = MongoClient(
            'mongodb://mongo1:27017,node2:27017,node3:27017/?replicaSet=myReplicaSet'
        )
        self.db = self.client[settings.mongo.database]

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

    def get_reviews_by_user(self, data) -> dict:
        collection = self.db["reviews"]
        response = collection.find_one({"user_uuid": data.user_uuid})
        return json.loads(json_util.dumps(response))

    def get_bookmarks_by_user(self, data) -> dict:
        collection = self.db["bookmarks"]
        response = collection.find_one({"user_uuid": data.user_uuid})
        return json.loads(json_util.dumps(response))

    def get_films_by_user(self, data) -> dict:
        collection = self.db["films"]
        response = collection.find_one({"user_uuid": data.user_uuid})
        return json.loads(json_util.dumps(response))

    def get_films_by_film(self, data) -> dict:
        collection = self.db["films"]
        response = collection.find_one({"film_id": data.user_uuid})
        return json.loads(json_util.dumps(response))


@lru_cache()
def get_mongo_service() -> MongoService:
    return MongoService()
