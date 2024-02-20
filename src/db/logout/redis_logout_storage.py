
from configs.settings import RedisLogoutSettings
from db.logout.logout_storage import LogoutStorage
from redis.asyncio import Redis


class RedisLogoutStorage(LogoutStorage):
    _settings = RedisLogoutSettings()


