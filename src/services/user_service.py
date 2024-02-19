from functools import lru_cache

from fastapi.responses import Response, JSONResponse

from db.auth.user import User
from db.models.auth_requests.user_request import UserRequest
from db.models.auth_requests.user_update_request import UserUpdateRequest
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

        # Существует ли пользователь с таким login
        user: User | Response = await self._postgres.get_single_data(
            field_name='login',
            field_value=login
        )
        if isinstance(user, User):
            return Response(status_code=409)  # User already exists

        # todo проверка валидности полей

        # Создать нового пользователя
        response: Response = await self._postgres.add_data(request)

        # Вернуть UUID нового пользователя
        new_user: User | Response = await self._postgres.get_single_data(
            field_name='login',
            field_value=login
        )
        if isinstance(new_user, Response):
            # todo когда пользователь добавлен, но uuid не получен
            #  (м.б. соединение, например)
            return JSONResponse(
                status_code=new_user.status_code,
                content={'uuid': 'CHECK ERROR'}
            )
        return JSONResponse(status_code=201, content={'uuid': str(new_user.uuid)})

    async def get_user_by_uuid(self, uuid: str) -> dict | Response:
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

    async def remove_account(self, uuid: str) -> Response:
        response: Response = await self._postgres.delete_single_data(uuid)
        return response

    async def authenticate(self, login: str, password: str) -> Response:
        result: User | Response = await self._postgres.get_single_data(
            field_name='login',
            field_value=login
        )
        if isinstance(result, Response):
            return result

        # todo is_password_correct: bool = result.check_password(password) - хеш
        if result.password == password:
            # todo будет создаваться токен
            return Response(status_code=201)  # Login OK
        else:
            return Response(status_code=400)  # Password is incorrect

    async def update_profile(
            self,
            uuid: str,
            login: str,
            first_name: str,
            last_name: str
    ) -> Response:
        # поменять логин и другие данные, кроме пароля
        request: UserUpdateRequest = UserUpdateRequest(
            uuid=uuid,
            login=login,
            first_name=first_name,
            last_name=last_name
        )
        result: Response = await self._postgres.update_single_data(request)
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
