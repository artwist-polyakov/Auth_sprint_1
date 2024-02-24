from abc import ABC

from db.cache.cache_storage import CacheStorage
from db.search.search_storage import SearchStorage
from elasticsearch import AsyncElasticsearch


class BaseService(ABC):

    # todo поменять имя переменной __elastic, когда абстрагируемся
    #  от конкретной реализации сделать просто _search
    #
    def __init__(self, cache: CacheStorage, search: AsyncElasticsearch | SearchStorage):
        self._cache = cache
        self._search = search
