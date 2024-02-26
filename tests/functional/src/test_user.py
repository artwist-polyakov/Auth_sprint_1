from http import HTTPStatus

import pytest
from configs.test_settings import settings


# POST
# /auth/v1/users/sign_up
# Sign Up

# GET
# /auth/v1/users/user
# Get User by UUID

# DELETE
# /auth/v1/users/delete
# Delete User by UUID

# GET
# /auth/v1/users/login
# Login

# PATCH
# /auth/v1/users/update
# Update Profile Data


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
    url = settings.auth_url + '/sign_up/'


@pytest.mark.asyncio
async def test_sign_up_repeated():
    """
    Тест проверяет, что на повторный запрос
    POST /auth/v1/users/sign_up?email=starfish%40mail.ru&password=Aa123
    1) возвращается строка
        "user with this email already exists"
    2) возвращается HTTPStatus.CONFLICT
    """
    url = settings.auth_url + '/sign_up/'


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
    url = settings.auth_url + '/sign_up/'


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
    url = settings.auth_url + '/sign_up/'


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
    url = settings.auth_url + '/login/'


@pytest.mark.asyncio
async def test_login_incorrect_password():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=starfish2%40mail.ru&password=aa
    1) возвращается "password is incorrect"
    2) возвращается HTTPStatus.BAD_REQUEST
    """
    url = settings.auth_url + '/login/'

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
    url = settings.auth_url + '/user/'


@pytest.mark.asyncio
async def test_user_no_token():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = settings.auth_url + '/user/'


@pytest.mark.asyncio
async def test_user_no_token_incorrect_uuid():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<wrong_uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = settings.auth_url + '/user/'


@pytest.mark.asyncio
async def test_user_correct_token_another_uuid():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<another_uuid>
    1) возвращается "Your access token doesn't permit request to this user"
    2) возвращается HTTPStatus.FORBIDDEN
    """
    url = settings.auth_url + '/user/'


@pytest.mark.asyncio
async def test_update_wrong_token():
    """
    Тест проверяет, что на запрос
    PATCH /auth/v1/users/update?uuid=<uuid>&email=starfish1000%40mail.ru
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = settings.auth_url + '/update/'


@pytest.mark.asyncio
async def test_update_correct():
    """
    Тест проверяет, что на запрос
    PATCH /auth/v1/users/update?uuid=<uuid>&email=starfish1000%40mail.ru
    'Cookie: access_token=<access_token>'
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = settings.auth_url + '/update/'


@pytest.mark.asyncio
async def test_delete_no_token():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = settings.auth_url + '/delete/'


@pytest.mark.asyncio
async def test_delete_incorrect_uuid():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<wrong_uuid>
    1) возвращается "Your access token doesn't permit request to this user"
    2) возвращается HTTPStatus.FORBIDDEN
    """
    url = settings.auth_url + '/delete/'


@pytest.mark.asyncio
async def test_delete_correct():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<uuid>
    с корректным access_cookie
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = settings.auth_url + '/delete/'
