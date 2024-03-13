from abc import ABC, abstractmethod

from db.models.oauth_models.oauth_token import OAuthToken


class OAuthRepository(ABC):

    @abstractmethod
    async def exchange_code(self, code: str) -> OAuthToken:
        pass

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> OAuthToken:
        pass

    @abstractmethod
    async def revoke_token(self, token: str) -> None:
        pass

    @abstractmethod
    async def get_user_info(self, token: str) -> dict:
        pass
