from abc import ABC, abstractmethod

from db.auth.user import User
from db.models.oauth_models.oauth_token import OAuthToken
from db.models.oauth_models.user_model import OAuthUserModel
from db.models.token_models.access_token_container import AccessTokenContainer
from db.postgres import PostgresInterface
from services.base_auth_service import BaseAuthService


class OAUTHService(BaseAuthService, ABC):

    def __init__(
            self,
            instance: PostgresInterface,
            oauth_method: str
    ):
        super().__init__(instance)
        self._oauth_method = oauth_method

    @abstractmethod
    async def exchange_code_for_tokens(
            self,
            code: str,
            device_type: str
    ) -> AccessTokenContainer | dict:
        pass

    async def _emit_user_token(
            self,
            user: User | dict,
            user_info: OAuthUserModel,
            tokens: OAuthToken,
            user_device_type: str
    ) -> AccessTokenContainer | None:
        if isinstance(user, User):
            await self._save_user_to_oauth(user_info, tokens, str(user.uuid))
            return await self._add_refresh_token(user, user_device_type)
        return None
