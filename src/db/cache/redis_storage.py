import logging

from redis.asyncio import Redis

from configs.settings import RedisCacheSettings
from db.cache.cache_storage import CacheStorage
from db.redis_core import RedisCore
from utils.wrappers import backoff


class RedisStorage(CacheStorage, RedisCore):
    _settings = RedisCacheSettings()

    @RedisCore.initialize
    @backoff(max_attempts=3)
    async def get_cache(self, key: str) -> str | None:
        return await self._redis.get(key)

    @RedisCore.initialize
    @backoff(max_attempts=3)
    async def put_cache(self, key: str, value: str, expired: int = 0) -> None:
        if expired > 0:
            await self._redis.set(key, value, ex=expired)
        elif expired == 0:
            await self._redis.set(key, value)
        else:
            logging.error(f"expired value should be greater than 0, "
                          f"but {expired} was passed")

    @RedisCore.initialize
    @backoff(max_attempts=3)
    async def delete_cache(self, key: str) -> None:
        await self._redis.delete(key)

    async def close(self):
        if self._redis is not None:
            await self._redis.close()
