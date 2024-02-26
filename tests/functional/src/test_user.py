from http import HTTPStatus

import pytest
from configs.test_settings import settings


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
    Тест проверяет, что на ПОВТОРНЫЙ запрос
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

