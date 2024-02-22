import time

from configs.settings import RedisLogoutSettings
from db.logout.logout_storage import LogoutStorage
from db.models.token_models.access_token_container import AccessTokenContainer
from db.redis_core import RedisCore
from utils.wrappers import backoff


class RedisLogoutStorage(LogoutStorage):
    _settings = RedisLogoutSettings()

    @RedisCore.initialize
    @backoff()
    async def logout_current_session(self, access_token: AccessTokenContainer) -> None:
        key = f"session:{access_token.refresh_id}"
        value = time.time_ns()
        ex = self._settings.refresh_lifetime
        await self._redis.set(key, value, ex=ex)

    @RedisCore.initialize
    @backoff()
    async def logout_all_sessions(self, access_token: AccessTokenContainer) -> None:
        key = f"user:{access_token.user_id}"
        value = time.time_ns()
        ex = self._settings.refresh_lifetime
        await self._redis.set(key, value, ex=ex)

    @RedisCore.initialize
    @backoff()
    async def is_blacklisted(self, access_token: AccessTokenContainer) -> bool:
        is_blacklisted = (await self._check_session_blacklist(
            access_token
        ) or await self._check_user_blacklist(
            access_token
        )
                          )
        return is_blacklisted

    async def _check_session_blacklist(self, access_token: AccessTokenContainer) -> bool:
        key = f"session:{access_token.refresh_id}"
        value = await self._redis.get(key)
        return value is not None and int(value) > access_token.created_at

    async def _check_user_blacklist(self, access_token: AccessTokenContainer) -> bool:
        key = f"user:{access_token.user_id}"
        value = await self._redis.get(key)
        return value is not None and int(value) > access_token.created_at

    async def close(self):
        if self._redis is not None:
            await self._redis.close()
