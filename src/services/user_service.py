from sqlalchemy.ext.asyncio import AsyncSession

from db.auth.user_storage import UserStorage
from db.models.auth_requests.requests import SignUpRequest
from db.models.auth_responses.auth_answers.signup_answers import SignUpAnswer


class UserService:
    def __init__(self, postgres: AsyncSession | UserStorage):
        self._postgres = postgres

    async def sign_up(self, data: dict):
        request = SignUpRequest(
            login=data['login'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        # проверка

        result = await self._postgres.handle_request(request)
        return SignUpAnswer if result else None

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

    async def get_user_data(self):
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
