from abc import ABC, abstractmethod

from db.cache.cache_storage import CacheStorage
from db.search.elastic_storage import ElasticStorage


class Creator(ABC):
    @abstractmethod
    def get_cache_storage(self) -> CacheStorage:
        pass

    @abstractmethod
    def get_search_storage(self) -> ElasticStorage:
        pass
