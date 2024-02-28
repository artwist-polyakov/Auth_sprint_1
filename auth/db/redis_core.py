from abc import ABC
from functools import wraps

from configs.settings import RedisSettings
from redis.asyncio import Redis


class RedisCore(ABC):
    _settings = RedisSettings()
    _redis: Redis | None = None

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
