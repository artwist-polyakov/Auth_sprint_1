import asyncio
import logging
import time
from functools import lru_cache

from configs.settings import RedisRateLimitterSettings
from db.rate_limiter.rate_limiter import RateLimitter
from db.redis_core import RedisCore
from utils.wrappers import asyncbackoff

MINUTE = 60


class RedisRateLimiter(RateLimitter, RedisCore):
    _settings = RedisRateLimitterSettings()
    cleanup_interval = MINUTE

    def __init__(self):
        self._start_cleanup_task()

    @RedisCore.initialize
    @asyncbackoff(max_attempts=3)
    async def add_request(self, key: str, value: str, timeout: int = MINUTE) -> None:
        current_time = int(time.time())
        await self._redis.zadd(key, {value: current_time})
        await self._redis.zremrangebyscore(key, 0, current_time - timeout)

    @RedisCore.initialize
    @asyncbackoff(max_attempts=3)
    async def get_num_requests(self, key: str) -> int:
        return await self._redis.zcard(key)

    @RedisCore.initialize
    @asyncbackoff(max_attempts=3)
    async def is_within_limit(self, key: str, max_requests) -> bool:
        num_requests = await self.get_num_requests(key)
        logging.warning(f'num_requests: {num_requests}, key: {key}')
        return num_requests < max_requests

    async def _cleanup_task(self):
        while True:
            logging.warning('i am cleanup')
            current_time = int(time.time())
            keys = await self._redis.keys('*')
            for key in keys:
                await self._redis.zremrangebyscore(key, 0, current_time - self.cleanup_interval)
            await asyncio.sleep(self.cleanup_interval)

    def _start_cleanup_task(self):
        asyncio.create_task(self._cleanup_task())

    async def close(self):
        if self._redis is not None:
            await self._redis.close()


@lru_cache
def get_rate_limiter():
    return RedisRateLimiter()
