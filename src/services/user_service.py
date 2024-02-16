from db.models.auth_requests.user_request import UserRequest
from db.models.auth_responses.auth_answers.signup_answer import SignUpAnswer, SignUpAnswerModel
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
    ) -> SignUpAnswerModel:
        request = UserRequest(
            login=login,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # проверка

        result = await self._postgres.add_data(request)

        # проверка

        if result:
            answer = SignUpAnswer('success')
        else:
            answer = SignUpAnswer('fail')
        return answer.get_answer_model()

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
