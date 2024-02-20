from abc import ABC, abstractmethod

from db.auth.access_token_container import AccessTokenContainer


class LogoutStorage(ABC):
    @abstractmethod
    async def logout_current_session(self, access_token: AccessTokenContainer) -> None:
        pass

    @abstractmethod
    async def logout_all_sessions(self, access_token: AccessTokenContainer) -> None:
        pass

    @abstractmethod
    async def is_blacklisted(self, access_token: AccessTokenContainer) -> bool:
        pass
