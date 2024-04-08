import logging
import os

from configs.elastic_shemas_config import MOVIES_INDEX_SCHEMA
from configs.settings import ElasticSettings
from elasticsearch import Elasticsearch, helpers
from models.elastic_models import (DataclassForElastic, GenreElement,
                                   PersonIdName)
from utils.utils import backoff


class ElasticLoader:
    _data: list[DataclassForElastic] = []
    _film_documents: list[dict] = []
    _elastic_settings = ElasticSettings().model_dump()

    _movies_index_name = os.getenv("ELASTIC_MOVIES_INDEX")

    def __init__(self):
        self._es = Elasticsearch(**self._elastic_settings)
        self._check_index_exists()

    def charge_movies_data(self, data: list[DataclassForElastic]):
        self._data = data
        self._film_documents = []
        for item in self._data:
            self._film_documents.append(self._map_dataclass(item))

    @backoff()
    def load_data(self):
        actions = [
            {"_index": self._movies_index_name, "_id": item["id"], "_source": item}
            for item in self._film_documents
        ]
        helpers.bulk(self._es, actions)

    def _map_dataclass(self, dataclass: DataclassForElastic) -> dict:
        return {
            "id": str(dataclass.id),
            "imdb_rating": float(dataclass.imdb_rating),
            "genres": [self._genre_to_dict(genre) for genre in dataclass.genres],
            "title": dataclass.title,
            "description": dataclass.description,
            "directors_names": dataclass.directors,
            "actors_names": dataclass.actor_names,
            "writers_names": dataclass.writers_names,
            "actors": [self._id_name_to_dict(actor) for actor in dataclass.actors],
            "writers": [self._id_name_to_dict(writer) for writer in dataclass.writers],
            "directors": [
                self._id_name_to_dict(director) for director in dataclass.directors_list
            ],
        }

    @staticmethod
    def _id_name_to_dict(data: PersonIdName):
        return {"id": str(data.person_id), "name": data.name}

    @staticmethod
    def _genre_to_dict(data: GenreElement):
        return {"id": str(data.id), "name": data.name, "description": data.description}

    @backoff()
    def _check_index_exists(self):
        if not self._es.indices.exists(index=self._movies_index_name):
            self._create_index()

    @backoff()
    def _create_index(self):
        self._es.indices.create(index=self._movies_index_name, body=MOVIES_INDEX_SCHEMA)
        logging.info(f"ELASTIC Index {self._movies_index_name} created")
