import logging
import uuid
from functools import lru_cache
from http import HTTPStatus

import bcrypt

from configs.settings import get_settings
from db.auth.user import User
from db.logout.logout_storage import LogoutStorage
from db.models.auth_requests.user_request import UserRequest
from db.models.oauth_models.user_model import OAuthUserModel
from db.models.token_models.access_token_container import AccessTokenContainer
from db.oauth.yandex_oauth_repository import get_yandex_oauth_rep
from db.postgres import PostgresInterface
from services.models.signup import PasswordModel, SignupModel
from services.oauth_service import OAUTHService
from utils.creator_provider import get_creator


class YandexOAUTHService(OAUTHService):

    def __init__(
            self,
            instance: PostgresInterface,
            oauth_method: str = get_settings().yandex_oauth_method_name
    ):
        super().__init__(instance, oauth_method)

    async def exchange_code_for_tokens(
            self,
            code: str,
            device_type: str
    ) -> AccessTokenContainer | dict:
        tokens = await get_yandex_oauth_rep().exchange_code(code)
        user_info = OAuthUserModel(**await get_yandex_oauth_rep()
                                   .get_user_info(tokens.access_token))
        model = SignupModel(
            email=user_info.email,
            password=PasswordModel.generate_password(),
            first_name=user_info.first_name,
            last_name=user_info.last_name
        )
        exists: User | dict = await self._get_existing_user(model.email)

        checkup = await self._emit_user_token(exists, user_info, tokens, device_type)
        if checkup:
            return checkup

        password_hash = bcrypt.hashpw(model.password.encode(), bcrypt.gensalt())
        request = UserRequest(
            uuid=str(uuid.uuid4()),
            email=model.email,
            password=password_hash,
            first_name=model.first_name,
            last_name=model.last_name
        )
        logging.warning(request)
        response: dict = await self._postgres.add_single_data(request, 'user')
        if response['status_code'] == HTTPStatus.CREATED:
            exists = await self._get_existing_user(model.email)
            return await self._emit_user_token(exists, user_info, tokens, device_type)
        return response


@lru_cache
def get_yandex_oauth_service() -> YandexOAUTHService:
    postgres = get_creator().get_postgres_storage()
    return YandexOAUTHService(
        instance=postgres,
    )