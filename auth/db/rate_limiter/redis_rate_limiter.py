import time

from configs.settings import RedisRateLimitterSettings
from db.rate_limiter.rate_limiter import RateLimitter
from db.redis_core import RedisCore
from utils.wrappers import asyncbackoff

MINUTE = 60


class RedisRateLimiter(RateLimitter, RedisCore):
    _settings = RedisRateLimitterSettings()

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
        return num_requests < max_requests
