import logging
from functools import wraps

from redis.asyncio import Redis

from configs.settings import RedisCacheSettings
from db.cache.cache_storage import CacheStorage
from utils.wrappers import backoff


class RedisStorage(CacheStorage):
    _redis: Redis | None = None
    _settings = RedisCacheSettings()

    @staticmethod
    def initialize(func):
        @wraps(func)
        async def inner(self, *args, **kwargs):
            if self._redis is None:
                self._redis = await Redis(
                    host=self._settings.host,
                    port=self._settings.port,
                    db=self._settings.db,
                ).initialize()
            return await func(self, *args, **kwargs)

        return inner

    @initialize
    @backoff(max_attempts=3)
    async def get_cache(self, key: str) -> str | None:
        return await self._redis.get(key)

    @initialize
    @backoff(max_attempts=3)
    async def put_cache(self, key: str, value: str, expired: int = 0) -> None:
        if expired > 0:
            await self._redis.set(key, value, ex=expired)
        elif expired == 0:
            await self._redis.set(key, value)
        else:
            logging.error(f"expired value should be greater than 0, "
                          f"but {expired} was passed")

    @initialize
    @backoff(max_attempts=3)
    async def delete_cache(self, key: str) -> None:
        await self._redis.delete(key)

    async def close(self):
        if self._redis is not None:
            await self._redis.close()
