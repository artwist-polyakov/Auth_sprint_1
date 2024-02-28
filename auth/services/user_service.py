import uuid
from datetime import datetime, timedelta
from functools import lru_cache
from http import HTTPStatus

import bcrypt
from configs.settings import settings
from db.auth.user import User
from db.logout.logout_storage import LogoutStorage
from db.models.auth_requests.user_request import UserRequest
from db.models.auth_requests.user_update_request import UserUpdateRequest
from db.models.auth_responses.user_response import UserResponse
from db.models.token_models.access_token_container import AccessTokenContainer
from db.models.token_models.refresh_token import RefreshToken
from db.postgres import PostgresInterface
from middlewares.rbac import has_permission
from services.models.permissions import RBACInfo
from services.models.signup import ProfileModel, SignupModel
from utils.creator_provider import get_creator

PAGE_SIZE = 10


def generate_access_container(user_id: str, refresh_id: str) -> AccessTokenContainer:
    result = AccessTokenContainer(
        user_id=user_id,
        role="user",
        is_superuser=False,
        verified=True,
        subscribed=False,
        created_at=int(datetime.now().timestamp()),
        refresh_id=refresh_id,
        refreshed_at=int(datetime.now().timestamp())
    )
    return result


class UserService:
    def __init__(self, instance: PostgresInterface, enters_storage: LogoutStorage):
        self._postgres = instance
        self._enters_storage = enters_storage

    async def sign_up(
            self,
            email: str,
            password: str,
            first_name: str = '',
            last_name: str = ''
    ) -> dict:
        model = SignupModel(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        exists: User | dict = await self._postgres.get_single_user(
            field_name='email',
            field_value=model.email
        )
        if isinstance(exists, User):
            return {
                'status_code': HTTPStatus.CONFLICT,
                'content': 'user with this email already exists'
            }
        password_hash = bcrypt.hashpw(model.password.encode(), bcrypt.gensalt())
        request = UserRequest(
            uuid=str(uuid.uuid4()),
            email=model.email,
            password=password_hash,
            first_name=model.first_name,
            last_name=model.last_name
        )
        response: dict = await self._postgres.add_single_data(request, 'user')
        match response['status_code']:
            case HTTPStatus.CREATED:
                content = {
                    'uuid': str(request.uuid),
                }
            case _:
                content = response['content']
        return {
            'status_code': response['status_code'],
            'content': content
        }

    async def get_user_by_uuid(self, uuid: str) -> dict:
        result: User | dict = await self._postgres.get_single_user(
            field_name='uuid',
            field_value=uuid
        )
        if isinstance(result, dict):
            return result
        response = UserResponse(
            uuid=str(result.uuid),
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name
        )
        return {
            'status_code': HTTPStatus.OK,
            'content': response.model_dump()
        }

    async def remove_account(self, uuid: str) -> dict:
        response: dict = await self._postgres.delete_single_data(uuid, 'user')
        return response

    async def authenticate(self, email: str, password: str) -> AccessTokenContainer | dict:
        user: User | dict = await self._postgres.get_single_user(
            field_name='email',
            field_value=email.lower()
        )
        if isinstance(user, dict):
            return user

        valid = bcrypt.checkpw(password.encode(), user.password.encode())
        if not valid:
            return {'status_code': HTTPStatus.BAD_REQUEST, 'content': 'password is incorrect'}

        refresh_token = RefreshToken(
            uuid=str(uuid.uuid4()),
            user_id=str(user.uuid),
            active_till=int((datetime.now() + timedelta(
                minutes=settings.refresh_token_expire_minutes)).timestamp())
        )
        await self._postgres.add_single_data(refresh_token, 'refresh_token')

        result = AccessTokenContainer(
            user_id=str(user.uuid),
            role="user",
            is_superuser=user.is_superuser,
            verified=True,
            subscribed=False,
            created_at=int(datetime.now().timestamp()),
            refresh_id=str(refresh_token.uuid),
            refreshed_at=int(datetime.now().timestamp())
        )
        return result

    async def update_profile(
            self,
            uuid: str,
            email: str,
            first_name: str,
            last_name: str
    ) -> dict:

        model = ProfileModel(
            email=email,
            uuid=uuid,
            first_name=first_name,
            last_name=last_name
        )

        # поменять логин и другие данные, кроме пароля
        request: UserUpdateRequest = UserUpdateRequest(
            uuid=model.uuid,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name
        )
        result: dict = await self._postgres.update_single_user(request)
        return result

    async def change_password(self, user_id: str, old_password: str, new_password: str):
        # Получение пользователя по user_id
        user = await self._postgres.get_single_user('uuid', user_id)
        if isinstance(user, dict):
            return {
                'status_code': HTTPStatus.NOT_FOUND,
                'content': 'User not found'
            }

        # Проверка текущего пароля
        valid_password = bcrypt.checkpw(old_password.encode(), user.password.encode())
        if not valid_password:
            return {
                'status_code': HTTPStatus.BAD_REQUEST,
                'content': 'Incorrect password'
            }

        # Обновление пароля
        new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        user.password = new_password_hash
        await self._postgres.update_single_user(user)
        return {
            'status_code': HTTPStatus.OK,
            'content': 'Password changed successfully'
        }

    async def refresh_access_token(self, refresh_id: str, user_id: str, active_till: int):
        if active_till < int(datetime.now().timestamp()):
            return {
                'status_code': HTTPStatus.UNAUTHORIZED,
                'content': 'Refresh token has expired'
            }

        token_to_blacklist = generate_access_container(user_id, refresh_id)
        await self._enters_storage.logout_current_session(token_to_blacklist)

        new_refresh_token = RefreshToken(
            uuid=refresh_id,
            user_id=user_id,
            active_till=int((datetime.now() + timedelta(
                minutes=settings.refresh_token_expire_minutes)).timestamp())
        )
        await self._postgres.update_refresh_token(new_refresh_token, refresh_id)

        # todo  добавить информацию про роль данного пользователя

        result = AccessTokenContainer(
            user_id=user_id,
            role="user",
            is_superuser=False,
            verified=True,
            subscribed=False,
            created_at=int(datetime.now().timestamp()),
            refresh_id=str(new_refresh_token.uuid),
            refreshed_at=int(datetime.now().timestamp())
        )
        return result

    async def logout_session(self, token_container: AccessTokenContainer):
        await self._enters_storage.logout_current_session(token_container)
        return {
            'status_code': HTTPStatus.OK,
            'content': 'Logout successfully'
        }

    async def logout_all_sessions(self, token_container: AccessTokenContainer):
        await self._enters_storage.logout_all_sessions(token_container)
        return {
            'status_code': HTTPStatus.OK,
            'content': 'Logout successfully'
        }

    async def get_login_history(
            self,
            user_id: str,
            page: int = 1,
            size: int = PAGE_SIZE
    ) -> dict:
        history = await self._postgres.get_history(
            user_id,
            size,
            (page - 1) * size
        )
        return history

    async def check_permissions(self,
                                logout_info: AccessTokenContainer,
                                rbac: RBACInfo
                                ) -> bool:
        is_blacklisted = await self._enters_storage.is_blacklisted(logout_info)
        has_permissions = await has_permission(rbac.role, rbac.resource, rbac.verb)
        return not is_blacklisted and has_permissions


@lru_cache
def get_user_service():
    postgres = PostgresInterface()
    logout = get_creator().get_logout_storage()
    return UserService(postgres, logout)
