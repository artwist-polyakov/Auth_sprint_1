from db.auth.user_storage import UserStorage
from db.cache.cache_storage import CacheStorage
from db.creator import Creator
from db.logout.logout_storage import LogoutStorage
from db.search.elastic_storage import ElasticStorage
from db.search.search_storage import SearchStorage


class StoragesCreator(Creator):
    """
    класс, который следит, чтобы был только один экземпляр класса и ничего больше.

    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(StoragesCreator, cls).__new__(cls)
        return cls._instance

    def __init__(
            self,
            cache_provider: CacheStorage,
            search_provider: SearchStorage,
            logout_provider: LogoutStorage,
            users_provider: UserStorage):
        self._cache = cache_provider
        self._search = search_provider
        self._logout = logout_provider
        self._users = users_provider

    def get_cache_storage(self) -> CacheStorage:
        return self._cache

    def get_search_storage(self) -> ElasticStorage:
        return self._search

    def get_logout_storage(self) -> LogoutStorage:
        return self._logout

    def get_users_storage(self) -> UserStorage:
        return self._users
