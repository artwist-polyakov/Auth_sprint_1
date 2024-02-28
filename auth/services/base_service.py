from abc import ABC

from db.cache.cache_storage import CacheStorage


class BaseService(ABC):
    def __init__(self, cache: CacheStorage):
        self._cache = cache
