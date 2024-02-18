from functools import lru_cache

from fastapi import Response

from db.auth.user import User
from db.models.auth_requests.user_request import UserRequest
from db.models.auth_responses.user_response import UserResponse
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
    ) -> Response:
        request = UserRequest(
            login=login,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_verified=True  # аккаунт всегда подтвержден
        )

        # Проверить, существует ли пользователь с таким login
        user: User | Response = await self._postgres.get_single_data(
            field_name='login',
            field_value=login
        )
        if isinstance(user, User):
            return Response(status_code=409)

        # todo проверка валидности полей

        # Создать нового пользователя
        response: Response = await self._postgres.add_data(request)
        return response

    async def get_user_by_uuid(
            self,
            uuid: str
    ) -> dict | Response:
        result: User | Response = await self._postgres.get_single_data(
            field_name='uuid',
            field_value=uuid
        )
        if isinstance(result, Response):
            return result
        response = UserResponse(
            uuid=str(result.uuid),
            login=result.login,
            first_name=result.first_name,
            is_verified=result.is_verified
        )
        return response.model_dump()

    async def remove_account(
            self,
            uuid: str
    ) -> Response:
        response: Response = await self._postgres.delete_single_data(uuid)
        return response

    async def login(self):
        pass

    async def logout(self):
        pass

    async def update_profile(self):
        # поменять логин и другие данные, кроме пароля
        pass

    async def change_password(self):
        pass

    async def reset_password(self):
        pass

    async def list_users(self):
        # список пользователей, только для администраторов
        pass

    async def associate_role(self):
        # функция для назначения ролей пользователям
        pass


@lru_cache
def get_user_service():
    postgres = PostgresProvider()
    return UserService(postgres)
