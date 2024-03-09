from configs.settings import RedisRateLimitterSettings
from db.rate_limiter.rate_limiter import RateLimitter
from db.redis_core import RedisCore


class RedisRateLimiter(RateLimitter, RedisCore):
    _settings = RedisRateLimitterSettings()
