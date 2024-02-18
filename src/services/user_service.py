from functools import lru_cache

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
    ) -> str:
        request = UserRequest(
            login=login,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_verified=True  # аккаунт всегда подтвержден
        )

        # todo проверка, что пользователь с таким логином не существует

        # todo проверка валидности

        answer_type: str = await self._postgres.add_data(request)
        return answer_type

    async def get_user_by_uuid(
            self,
            uuid: str,
    ) -> dict | None:
        result: UserResponse | None = await self._postgres.get_single_data(
            field_name='uuid',
            field_value=uuid
        )
        if result:
            data = result.model_dump()
        else:
            data = None
        return data

    async def login(self):
        pass

    async def logout(self):
        pass

    async def remove_account(self):
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
