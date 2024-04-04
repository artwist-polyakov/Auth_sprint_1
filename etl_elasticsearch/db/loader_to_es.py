import abc
import logging

from configs.settings import ElasticSettings
from elasticsearch import Elasticsearch, helpers
from utils.utils import backoff


class ElasticLoader(abc.ABC):
    _index_name: str = ""
    _schema: dict = {}
    _dataclass = None
    _data: list[_dataclass] = []
    _documents: list[dict] = []
    _elastic_settings = ElasticSettings().model_dump()

    def __init__(self):
        self._es = Elasticsearch(**self._elastic_settings)
        self._check_index_exists()

    def charge_data(self, data: list[_dataclass]) -> None:
        self._data = data
        self._documents = []
        for item in self._data:
            self._documents.append(self._map_dataclass(item))

    @backoff()
    def load_data(self) -> None:
        actions = [
            {"_index": self._index_name, "_id": item["id"], "_source": item}
            for item in self._documents
        ]
        helpers.bulk(self._es, actions)

    @abc.abstractmethod
    def _map_dataclass(self, dataclass: _dataclass) -> dict:
        pass

    @backoff()
    def _check_index_exists(self):
        if not self._es.indices.exists(index=self._index_name):
            self._create_index()

    @backoff()
    def _create_index(self):
        self._es.indices.create(index=self._index_name, body=self._schema)
        logging.info(f"ELASTIC Index {self._index_name} created")
