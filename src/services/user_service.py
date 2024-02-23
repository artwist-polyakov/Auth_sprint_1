import uuid
from datetime import datetime, timedelta
from functools import lru_cache

import bcrypt

from configs.settings import settings
from db.auth.user import User
from db.models.auth_requests.user_request import UserRequest
from db.models.auth_requests.user_update_request import UserUpdateRequest
from db.models.auth_responses.user_response import UserResponse
from db.models.token_models.access_token_container import AccessTokenContainer
from db.models.token_models.refresh_token import RefreshToken
from db.postgres import PostgresProvider
from services.models.signup import ProfileModel, SignupModel


class UserService:
    def __init__(self, instance: PostgresProvider):
        self._postgres = instance

    async def sign_up(
            self,
            login: str,
            password: str,
            first_name: str = '',
            last_name: str = ''
    ) -> dict:
        # todo проверка валидности полей

        model = SignupModel(
            login=login,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=None
        )

        exists: User | dict = await self._postgres.get_single_user(
            field_name='login',
            field_value=model.login
        )
        if isinstance(exists, User):
            return {
                'status_code': 409,
                'content': 'user with this login already exists'
            }
        password_hash = bcrypt.hashpw(model.password.encode(), bcrypt.gensalt())
        request = UserRequest(
            uuid=str(uuid.uuid4()),
            login=model.login,
            password=password_hash,
            first_name=model.first_name,
            last_name=model.last_name,
            is_verified=True  # аккаунт всегда подтвержден !! НАОБОРОТ по дефолту не !!
        )
        response: dict = await self._postgres.add_single_data(request, 'user')
        match response['status_code']:
            case 201:
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
            login=result.login,
            first_name=result.first_name,
            last_name=result.last_name
        )
        return {
            'status_code': 200,
            'content': response.model_dump()
        }

    async def remove_account(self, uuid: str) -> dict:
        response: dict = await self._postgres.delete_single_data(uuid)
        return response

    # todo сделаеть обёртку для ошибок или raise (я бы выбрал raise)
    async def authenticate(self, login: str, password: str) -> AccessTokenContainer | dict:
        user: User | dict = await self._postgres.get_single_user(
            field_name='login',
            field_value=login
        )
        if isinstance(user, dict):
            return user

        valid = bcrypt.checkpw(password.encode(), user.password.encode())
        if not valid:
            return {'status_code': 400, 'content': 'password is incorrect'}

        refresh_token = RefreshToken(
            uuid=str(uuid.uuid4()),
            user_id=str(user.uuid),
            active_till=int((datetime.now() + timedelta(
                minutes=settings.refresh_token_expire_minutes)).timestamp())
            # todo добавить в базу данные о дате создания рефреша
        )
        await self._postgres.add_single_data(refresh_token, 'refresh_token')

        result = AccessTokenContainer(
            user_id=str(user.uuid),
            role="user",
            is_superuser=False,
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
            login: str,
            first_name: str,
            last_name: str
    ) -> dict:

        model = ProfileModel(
            login=login,
            uuid=uuid,
            first_name=first_name,
            last_name=last_name
        )

        # поменять логин и другие данные, кроме пароля
        request: UserUpdateRequest = UserUpdateRequest(
            uuid=model.uuid,
            login=model.login,
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
                'status_code': 404,
                'content': 'User not found'
            }

        # Проверка текущего пароля
        valid_password = bcrypt.checkpw(old_password.encode(), user.password.encode())
        if not valid_password:
            return {
                'status_code': 400,
                'content': 'Incorrect password'
            }

        # Обновление пароля
        new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        user.password = new_password_hash
        await self._postgres.update_single_user(user)
        return {
            'status_code': 200,
            'content': 'Password changed successfully'
        }

    async def logout(self):
        # todo
        pass

    async def refresh_access_token(self, refresh_id: str, user_id: str, active_till: int):
        if active_till < int(datetime.now().timestamp()):
            return {
                'status_code': 401,
                'content': 'Refresh token has expired'
            }
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


@lru_cache
def get_user_service():
    postgres = PostgresProvider()
    return UserService(postgres)
