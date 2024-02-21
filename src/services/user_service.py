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


class UserService:
    def __init__(self, instance: PostgresProvider):
        self._postgres = instance

    async def sign_up(
            self,
            login: str,
            password: str,
            first_name: str,
            last_name: str
    ) -> dict:
        # todo проверка валидности полей

        exists: User | dict = await self._postgres.get_single_user(
            field_name='login',
            field_value=login
        )
        if isinstance(exists, User):
            return {
                'status_code': 409,
                'content': 'user with this login already exists'
            }
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        request = UserRequest(
            uuid=str(uuid.uuid4()),
            login=login,
            password=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        response: dict = await self._postgres.add_single_data(request, 'user')
        match response['status_code']:
            case 201:
                access_token = AccessTokenContainer(
                    user_id=str(request.uuid),
                    role=["user"],
                    verified=True,
                    subscribed=False,
                    subscription_till=0,
                    created_at=int(datetime.utcnow().timestamp()),
                    refresh_id=str(uuid.uuid4()),
                )
                refresh_token = RefreshToken(
                    uuid=str(access_token.refresh_id),
                    user_id=str(request.uuid),
                    active_till=int((datetime.now() + timedelta(
                        minutes=settings.refresh_token_expire_minutes)).timestamp())
                )
                await self._postgres.add_single_data(refresh_token, 'refresh_token')
                content = {
                    'uuid': str(request.uuid),
                    'access_token': access_token,
                    'refresh_token': str(refresh_token.uuid)
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

    async def authenticate(self, login: str, password: str) -> dict:
        user: User | dict = await self._postgres.get_single_user(
            field_name='login',
            field_value=login
        )
        if isinstance(user, dict):
            return user

        valid = bcrypt.checkpw(password.encode(), user.password.encode())
        if not valid:
            return {'status_code': 400, 'content': 'password is incorrect'}

        access_token = AccessTokenContainer(
            user_id=str(user.uuid),
            role=["user"],
            created_at=int(datetime.now().timestamp()),
            refresh_id=str(uuid.uuid4())
        )
        refresh_token = RefreshToken(
            uuid=str(access_token.refresh_id),
            user_id=str(user.uuid),
            active_till=int((datetime.now() + timedelta(
                minutes=settings.refresh_token_expire_minutes)).timestamp())
        )
        await self._postgres.add_single_data(refresh_token, 'refresh_token')
        return {
            'status_code': 200,
            'content': {
                'access_token': access_token.model_dump(),
                'refresh_token': refresh_token.model_dump()
            }
        }

    async def update_profile(
            self,
            uuid: str,
            login: str,
            first_name: str,
            last_name: str
    ) -> dict:
        # поменять логин и другие данные, кроме пароля
        request: UserUpdateRequest = UserUpdateRequest(
            uuid=uuid,
            login=login,
            first_name=first_name,
            last_name=last_name
        )
        result: dict = await self._postgres.update_single_user(request)
        return result

    async def update_tokens(self, refresh_token: str):
        old_refresh_token = await self._postgres.get_refresh_token(refresh_token)
        if not old_refresh_token:
            return {
                'status_code': 401,
                'content': 'Invalid refresh token'
            }

        if old_refresh_token.active_till < int(datetime.now().timestamp()):
            return {
                'status_code': 401,
                'content': 'Refresh token has expired'
            }

        new_access_token = AccessTokenContainer(
            user_id=str(old_refresh_token.user_id),
            created_at=int(datetime.now().timestamp()),
            refresh_id=str(old_refresh_token.uuid)
        )

        new_refresh_token = RefreshToken(
            uuid=str(old_refresh_token.uuid),
            user_id=str(old_refresh_token.user_id),
            active_till=int((datetime.now() + timedelta(
                minutes=settings.refresh_token_expire_minutes)).timestamp())
        )

        # Запись нового refresh токена в постгрес
        await self._postgres.update_refresh_token(new_refresh_token)

        return {
            'status_code': 200,
            'content': {
                'access_token': new_access_token.model_dump(),
                'refresh_token': new_refresh_token.model_dump()
            }
        }

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


@lru_cache
def get_user_service():
    postgres = PostgresProvider()
    return UserService(postgres)
