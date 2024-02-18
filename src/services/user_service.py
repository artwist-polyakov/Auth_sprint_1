from functools import lru_cache

from fastapi import Response, status

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

        user: User | None = await self._postgres.get_single_data(
            field_name='login',
            field_value=login
        )
        if user:
            return Response(content='', status_code=status.HTTP_409_CONFLICT)

        # todo проверка валидности

        response: Response = await self._postgres.add_data(request)
        return response

    async def get_user_by_uuid(
            self,
            uuid: str
    ) -> dict | None:
        user: User | None = await self._postgres.get_single_data(
            field_name='uuid',
            field_value=uuid
        )
        if not user:
            return None
        response = UserResponse(
            uuid=str(user.uuid),
            login=user.login,
            first_name=user.first_name,
            is_verified=user.is_verified
        )
        return response.model_dump()

    async def remove_account(
            self,
            uuid: str
    ) -> Response:
        response = await self._postgres.delete_single_data(uuid)
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

    async def delete_account(self):
        pass

    async def associate_role(self):
        # функция для назначения ролей пользователям
        pass

    async def check_password(self):
        pass


@lru_cache
def get_user_service():
    postgres = PostgresProvider()
    return UserService(postgres)
