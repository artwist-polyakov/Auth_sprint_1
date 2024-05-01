from abc import ABC

from db.cache.cache_storage import CacheStorage
from db.search.search_storage import SearchStorage
from elasticsearch import AsyncElasticsearch


class BaseService(ABC):

    def __init__(self, cache: CacheStorage, search: AsyncElasticsearch | SearchStorage):
        self._cache = cache
        self._search = search
