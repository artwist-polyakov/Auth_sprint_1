import uuid
from abc import ABC
from abc import abstractmethod

from db.auth.user import User
from db.models.oauth_models.oauth_db import OAuthDBModel
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

    async def _save_user_to_oauth(
            self,
            user_info: OAuthUserModel,
            tokens: OAuthToken,
            user_id: str
    ) -> bool:
        exists = await self._postgres.get_yandex_oauth_user(user_info.email)
        if exists:
            return False
        model = OAuthDBModel(
            uuid=str(uuid.uuid4()),
            email=user_info.email,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            oauth_source=self._oauth_method,
            token_type=tokens.token_type,
            expires_in=tokens.expires_in,
            user_id=user_id
        )
        await self._postgres.add_single_data(model, 'oauth')
        return True
