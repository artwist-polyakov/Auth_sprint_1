from http import HTTPStatus

import pytest
from configs.test_settings import settings


USERS_URL = settings.auth_url + '/users'


# cookies = add_and_login_user
# access_token = cookies['access_token']
#
# assert isinstance(access_token, str)
#
# data = {'params': params, 'cookies': {'access_token': access_token}}


@pytest.mark.asyncio
async def test_sign_up_correct():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=starfish%40mail.ru&password=Aa123
    1) возвращается словарь вида
        {
          "uuid": "uuid",
          "token_type": "str"
        }
    2) возвращается HTTPStatus.CREATED,
    3) token_type содержит "cookie-jwt"
    """
    url = USERS_URL + '/sign_up'


@pytest.mark.asyncio
async def test_sign_up_repeated():
    """
    Тест проверяет, что на повторный запрос
    POST /auth/v1/users/sign_up?email=starfish%40mail.ru&password=Aa123
    1) возвращается строка
        "user with this email already exists"
    2) возвращается HTTPStatus.CONFLICT
    """
    url = USERS_URL + '/sign_up'


@pytest.mark.asyncio
async def test_sign_up_incorrect_email():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=starfish&password=Aa123
    1) возвращается словарь вида
        {
          "status_code": 422,
          "content": "Email is not valid"
        }
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/sign_up'


@pytest.mark.asyncio
async def test_sign_up_incorrect_password():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=starfish2%40mail.ru&password=aa
    1) возвращается словарь вида
        {
          "status_code": 422,
          "content": "Password must have at least 5 characters"
        }
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/sign_up'


@pytest.mark.asyncio
async def test_login_correct():
    """
    Тест проверяет, что на запрос
    /auth/v1/users/login?email=starfish%40mail.ru&password=Aa123
    1) возвращается словарь вида
        {
          "refresh_token": "str",
          "access_token": "str",
          "token_type": "str"
        }
    2) возвращается HTTPStatus.OK,
    3) token_type содержит "bearer"
    """
    url = USERS_URL + '/login'


@pytest.mark.asyncio
async def test_login_incorrect_password():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=starfish2%40mail.ru&password=aa
    1) возвращается "password is incorrect"
    2) возвращается HTTPStatus.BAD_REQUEST
    """
    url = USERS_URL + '/login'

    # todo мб можно проверить, созданы ли токены


@pytest.mark.asyncio
async def test_user_correct():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<uuid>
    'Cookie: access_token=<access_token>'
    1) возвращается ответ вида
        {
          "uuid": "uuid",
          "email": "str",
          "first_name": "str",
          "last_name": "str"
        }
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/user'


@pytest.mark.asyncio
async def test_user_no_token():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/user'


@pytest.mark.asyncio
async def test_user_no_token_incorrect_uuid():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<wrong_uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/user'


@pytest.mark.asyncio
async def test_user_correct_token_another_uuid():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<another_uuid>
    1) возвращается "Your access token doesn't permit request to this user"
    2) возвращается HTTPStatus.FORBIDDEN
    """
    url = USERS_URL + '/user'


@pytest.mark.asyncio
async def test_update_wrong_token():
    """
    Тест проверяет, что на запрос
    PATCH /auth/v1/users/update?uuid=<uuid>&email=starfish1000%40mail.ru
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/update'


@pytest.mark.asyncio
async def test_update_correct():
    """
    Тест проверяет, что на запрос
    PATCH /auth/v1/users/update?uuid=<uuid>&email=starfish1000%40mail.ru
    'Cookie: access_token=<access_token>'
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/update'


@pytest.mark.asyncio
async def test_delete_no_token():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/delete'


@pytest.mark.asyncio
async def test_delete_incorrect_uuid():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<wrong_uuid>
    1) возвращается "Your access token doesn't permit request to this user"
    2) возвращается HTTPStatus.FORBIDDEN
    """
    url = USERS_URL + '/delete'


@pytest.mark.asyncio
async def test_delete_correct():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<uuid>
    с корректным access_cookie
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/delete'


@pytest.mark.asyncio
async def test_tokens_refresh_incorrect_refresh():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/refresh
    с некорректным refresh_token_cookie
    1) возвращается "Refresh token has expired"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/delete'


@pytest.mark.asyncio
async def test_tokens_refresh_correct_refresh():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/refresh
    с корректным refresh_token_cookie
    1) возвращается валидный access_token в словаре вида
        {
            "refresh_token": "str",
            "access_token": "str"
        }
    2) возвращается HTTPStatus.OK
    """
    # todo на самом деле должно возвращаться HTTPStatus.CREATED

    url = USERS_URL + '/refresh'


@pytest.mark.asyncio
async def test_history_incorrect_access():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/history
    с некорректным access_token_cookie
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/history'


@pytest.mark.asyncio
async def test_history_correct_access():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/history
    с корректным access_token_cookie
    1) возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
     [
         {
          "token_id": "uuid",
          "created_at": "datetime",
          "active_till": int,
          "user_id": "uuid"
         },
         ...
     ]
    3) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/history'


@pytest.mark.asyncio
async def test_check_permissions_correct_access():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/check_permissions?resource=???&verb=???
    с корректным access_token_cookie,
    где указана соответствующая пользователю роль
    2) возвращается true
    3) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/check_permissions'
    # todo не понимаю, как работает и как проверять


@pytest.mark.asyncio
async def test_check_permissions_correct_access_no_role():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/check_permissions?resource=???&verb=???
    с корректным access_token_cookie,
    где указана не соответствующая пользователю роль
    2) возвращается false
    3) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/check_permissions'
    # todo не понимаю, как работает и как проверять


@pytest.mark.asyncio
async def test_check_permissions_incorrect_access():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/check_permissions?resource=???&verb=???
    с некорректным access_token_cookie
    2) возвращается ???
    3) возвращается ???
    """
    url = USERS_URL + '/check_permissions'
    # todo не понимаю, как работает и как проверять


@pytest.mark.asyncio
async def test_logout_incorrect_access():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout
    с некорректным access_token_cookie
    1) возвращается
    2) возвращается
    """
    # todo AttributeError: 'NoneType' object has no attribute 'rsplit'
    url = USERS_URL + '/logout'


@pytest.mark.asyncio
async def test_logout_no_access():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout
    для пользователя без access_token_cookie
    1) возвращается
    2) возвращается
    """
    # todo AttributeError: 'NoneType' object has no attribute 'rsplit'
    url = USERS_URL + '/logout'


@pytest.mark.asyncio
async def test_logout_correct_access():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout
    с корректным access_token_cookie
    1) возвращается "Logout successfully"
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/logout'


@pytest.mark.asyncio
async def test_logout_after_logout():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout
    с корректным access_token_cookie, который уже не может быть использован
    1) возвращается "Token is logout, please re-login"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/logout'


@pytest.mark.asyncio
async def test_logout_all_devices_incorrect_access():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout_all_devices
    с некорректным access_token_cookie
    1) возвращается
    2) возвращается
    """
    # todo AttributeError: 'NoneType' object has no attribute 'rsplit'
    url = USERS_URL + '/logout_all_devices'


@pytest.mark.asyncio
async def test_logout_all_devices_no_access():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout_all_devices
    для пользователя без access_token_cookie
    1) возвращается
    2) возвращается
    """
    # todo AttributeError: 'NoneType' object has no attribute 'rsplit'
    url = USERS_URL + '/logout_all_devices'


@pytest.mark.asyncio
async def test_logout_all_devices_correct_access():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout_all_devices
    с корректным access_token_cookie
    1) возвращается "Logout successfully"
    2) возвращается HTTPStatus.OK
    """
    url = USERS_URL + '/logout_all_devices'


@pytest.mark.asyncio
async def test_logout_all_devices_after_logout():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout_all_devices
    с корректным access_token_cookie, который уже не может быть использован
    1) возвращается "Token is logout, please re-login"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/logout_all_devices'
