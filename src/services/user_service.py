from functools import lru_cache

import bcrypt

from db.auth.user import User
from db.models.auth_requests.user_request import UserRequest
from db.models.auth_requests.user_update_request import UserUpdateRequest
from db.models.auth_responses.user_response import UserResponse
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

        exists: User | dict = await self._postgres.get_single_data(
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
            login=model.login,
            password=password_hash,
            first_name=model.first_name,
            last_name=model.last_name,
            is_verified=True  # аккаунт всегда подтвержден !! НАОБОРОТ по дефолту не !!
        )
        response: dict = await self._postgres.add_single_data(request)
        match response['status_code']:
            case 201:
                content = {'uuid': str(request.uuid)}
            case _:
                content = response['content']
        return {
            'status_code': response['status_code'],
            'content': content
        }

    async def get_user_by_uuid(self, uuid: str) -> dict:
        result: User | dict = await self._postgres.get_single_data(
            field_name='uuid',
            field_value=uuid
        )
        if isinstance(result, dict):
            return result
        response = UserResponse(
            uuid=str(result.uuid),
            login=result.login,
            first_name=result.first_name,
            last_name=result.last_name,
            is_verified=result.is_verified
        )
        return {
            'status_code': 200,
            'content': response.model_dump()
        }

    async def remove_account(self, uuid: str) -> dict:
        response: dict = await self._postgres.delete_single_data(uuid)
        return response

    async def authenticate(self, login: str, password: str) -> dict:
        result: User | dict = await self._postgres.get_single_data(
            field_name='login',
            field_value=login
        )
        if isinstance(result, dict):
            return result

        valid = bcrypt.checkpw(password.encode(), result.password.encode())
        if valid:
            # todo будет создаваться токен
            return {'status_code': 200, 'content': 'authenticated'}
        else:
            return {'status_code': 400, 'content': 'password is incorrect'}

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
        result: dict = await self._postgres.update_single_data(request)
        return result

    async def change_password(self):
        # todo хеш
        pass

    async def logout(self):
        # todo работа с токенами
        pass

    async def reset_password(self):
        # todo работа с токенами?
        pass


@lru_cache
def get_user_service():
    postgres = PostgresProvider()
    return UserService(postgres)
