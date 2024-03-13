import uuid
from abc import ABC
from datetime import datetime, timedelta

from configs.settings import settings
from db.auth.user import User
from db.models.oauth_models.oauth_db import OAuthDBModel
from db.models.oauth_models.oauth_token import OAuthToken
from db.models.oauth_models.user_model import OAuthUserModel
from db.models.token_models.access_token_container import AccessTokenContainer
from db.models.token_models.refresh_token import RefreshToken
from db.postgres import PostgresInterface


class BaseAuthService(ABC):

    def __init__(
            self,
            instance: PostgresInterface,
    ):
        self._postgres = instance

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

    async def _add_refresh_token(self, user: User, device_type: str) -> AccessTokenContainer:
        refresh_token = RefreshToken(
            uuid=str(uuid.uuid4()),
            user_id=str(user.uuid),
            active_till=int((datetime.now() + timedelta(
                minutes=settings.refresh_token_expire_minutes)).timestamp()),
            user_device_type=device_type
        )
        await self._postgres.add_single_data(refresh_token, 'refresh_token')
        return AccessTokenContainer(
            user_id=str(user.uuid),
            role=user.role,
            is_superuser=user.is_superuser,
            verified=True,
            subscribed=False,
            created_at=int(datetime.now().timestamp()),
            refresh_id=str(refresh_token.uuid),
            refreshed_at=int(datetime.now().timestamp()),
            user_device_type=device_type
        )

    async def _get_existing_user(self, email: str) -> User | dict:
        return await self._postgres.get_single_user('email', email)

    def _generate_access_container(
            self,
            user_id: str,
            refresh_id: str,
            user_device_type: str
    ) -> AccessTokenContainer:
        result = AccessTokenContainer(
            user_id=user_id,
            role="user",
            is_superuser=False,
            verified=True,
            subscribed=False,
            created_at=int(datetime.now().timestamp()),
            refresh_id=refresh_id,
            refreshed_at=int(datetime.now().timestamp()),
            user_device_type=user_device_type
        )
        return result
