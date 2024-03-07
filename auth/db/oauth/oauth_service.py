from abc import abstractmethod, ABC

from db.models.token_models.oauth_token import OAuthToken


class OAuthService(ABC):

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