from abc import abstractmethod, ABC

from db.models.token_models.oauth_token import OAuthToken


class OAuthService(ABC):

    @abstractmethod
    async def exchange_code(self, code: str) -> OAuthToken:
        pass