import random
import uuid
from http import HTTPStatus

import pytest
from configs.test_settings import settings
from src.tests_basic_functions import (check_pagination, create_user,
                                       get_response)

USERS_URL = settings.auth_url + '/users'


@pytest.mark.asyncio
async def test_sign_up_correct():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=<email>&password=Aa123
    1) возвращается словарь вида
        {
          "uuid": "uuid",
          "token_type": "str"
        }
    2) возвращается HTTPStatus.CREATED,
    3) token_type содержит "cookie-jwt"
    """
    body, status, _, _ = await create_user()

    assert status == HTTPStatus.CREATED
    assert isinstance(body, dict)
    assert 'uuid' in body, "'uuid' должен быть в ответе"
    assert 'token_type' in body, "'token_type' должен быть в ответе"
    assert isinstance(body['uuid'], str)
    assert isinstance(body['token_type'], str)
    assert body['token_type'] == 'cookie-jwt'


@pytest.mark.asyncio
async def test_sign_up_repeated():
    """
    Тест проверяет, что на повторный запрос
    POST /auth/v1/users/sign_up?email=<email>&password=Aa123
    1) возвращается строка
        "user with this email already exists"
    2) возвращается HTTPStatus.CONFLICT
    """
    random_five_digit_number = random.randint(10000, 99999)
    email = f'starfish{random_five_digit_number}@mail.ru'
    await create_user(email=email)

    body, status, _, _ = await create_user(email=email)

    assert status == HTTPStatus.CONFLICT
    assert isinstance(body, str)
    assert body == 'user with this email already exists'


@pytest.mark.asyncio
async def test_sign_up_incorrect_email():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=<wrong_email>&password=Aa123
    1) возвращается словарь вида
        {
          "status_code": 422,
          "content": "Email is not valid"
        }
    2) возвращается HTTPStatus.OK
    """
    body, status, _, _ = await create_user(email='aa')

    assert status == HTTPStatus.OK
    assert isinstance(body, dict)
    assert 'status_code' in body, "'status_code' должен быть в ответе"
    assert 'content' in body, "'content' должен быть в ответе"
    assert body['status_code'] == 422
    assert body['content'] == 'Email is not valid'


@pytest.mark.asyncio
async def test_sign_up_wrong_password():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/sign_up?email=<email>&password=aa
    1) возвращается словарь вида
        {
          "status_code": 422,
          "content": "Password must have at least 5 characters"
        }
    2) возвращается HTTPStatus.OK
    """
    body, status, _, _ = await create_user(password='aa')

    assert status == HTTPStatus.OK
    assert isinstance(body, dict)
    assert 'status_code' in body, "'status_code' должен быть в ответе"
    assert 'content' in body, "'content' должен быть в ответе"
    assert body['status_code'] == 422
    assert body['content'] == 'Password must have at least 5 characters'


@pytest.mark.asyncio
async def test_login_correct():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/login?email=<email>&password=Aa123
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
    _, _, email, password = await create_user()

    body, status = await get_response(
        method='GET',
        url=url,
        params={'email': email, 'password': password}
    )

    assert status == HTTPStatus.OK
    assert isinstance(body, dict)
    assert 'refresh_token' in body, "'refresh_token' должен быть в ответе"
    assert 'access_token' in body, "'access_token' должен быть в ответе"
    assert 'token_type' in body, "'token_type' должен быть в ответе"
    assert isinstance(body['refresh_token'], str), "refresh_token должен быть строкой"
    assert isinstance(body['access_token'], str), "access_token должен быть строкой"
    assert isinstance(body['token_type'], str), "token_type должен быть строкой"
    assert body['refresh_token'] != ''
    assert body['access_token'] != ''
    assert body['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_login_wrong_password():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/sign_up?email=<email>&password=aa
    1) возвращается "password is incorrect"
    2) возвращается HTTPStatus.BAD_REQUEST
    """
    _, _, email, _ = await create_user()
    url = USERS_URL + '/login'

    body, status = await get_response(
        method='GET',
        url=url,
        params={'email': email, 'password': 'aa'}
    )

    assert status == HTTPStatus.BAD_REQUEST
    assert isinstance(body, str)
    assert body == 'password is incorrect'


@pytest.mark.asyncio
async def test_user_correct(login_user):
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
    body, user_uuid, email, _ = login_user
    url = USERS_URL + '/user'

    body, status = await get_response(
        method='GET',
        url=url,
        params={'uuid': user_uuid},
        cookies={'access_token': body['access_token']}
    )

    assert status == HTTPStatus.OK
    assert isinstance(body, dict)
    assert 'uuid' in body
    assert 'email' in body
    assert 'first_name' in body
    assert 'last_name' in body
    assert body['uuid'] == user_uuid
    assert body['email'] == email
    assert isinstance(body['first_name'], str)
    assert isinstance(body['last_name'], str)


@pytest.mark.asyncio
async def test_user_no_token():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<uuid>
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    body, user_uuid, _, _ = await create_user()
    url = USERS_URL + '/user'

    body, status = await get_response(
        method='GET',
        url=url,
        params={'uuid': user_uuid}
    )

    assert status == HTTPStatus.UNAUTHORIZED
    assert body == 'Invalid access token'


@pytest.mark.asyncio
async def test_user_no_token_wrong_uuid():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<wrong_uuid>
    без access token
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/user'
    wrong_user_uuid = str(uuid.uuid4())

    body, status = await get_response(
        method='GET',
        url=url,
        params={'uuid': wrong_user_uuid}
    )

    assert status == HTTPStatus.UNAUTHORIZED
    assert body == 'Invalid access token'


@pytest.mark.asyncio
async def test_user_correct_token_wrong_uuid(login_user):
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/user?uuid=<another_uuid>
    1) возвращается "Your access token doesn't permit request to this user"
    2) возвращается HTTPStatus.FORBIDDEN
    """
    body, *args = login_user
    url = USERS_URL + '/user'
    wrong_user_uuid = str(uuid.uuid4())

    body, status = await get_response(
        method='GET',
        url=url,
        params={'uuid': wrong_user_uuid},
        cookies={'access_token': body['access_token']}
    )

    assert status == HTTPStatus.FORBIDDEN
    assert body == 'Your access token doesn\'t permit request to this user'


@pytest.mark.asyncio
async def test_update_no_token():
    """
    Тест проверяет, что на запрос
    PATCH /auth/v1/users/update?uuid=<uuid>&email=<email>
    без access token
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    body, user_uuid, email, _ = await create_user()
    url = USERS_URL + '/update'
    new_email = 'new' + email

    body, status = await get_response(
        method='PATCH',
        url=url,
        params={'uuid': user_uuid, 'email': new_email}
    )

    assert status == HTTPStatus.UNAUTHORIZED
    assert body == 'Invalid access token'


@pytest.mark.asyncio
async def test_update_correct(login_user):
    """
    Тест проверяет, что на запрос
    PATCH /auth/v1/users/update?uuid=<uuid>&email=<new_email>
    'Cookie: access_token=<access_token>'
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    body, user_uuid, email, _ = login_user
    url = USERS_URL + '/update'
    new_email = 'new' + email

    new_body, status = await get_response(
        method='PATCH',
        url=url,
        params={'uuid': user_uuid, 'email': new_email},
        cookies={'access_token': body['access_token']}
    )

    assert status == HTTPStatus.OK
    assert new_body == "success"


@pytest.mark.asyncio
async def test_delete_no_access():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<uuid>
    без access_token
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    _, user_uuid, _, _ = await create_user()
    url = USERS_URL + '/delete'

    body, status = await get_response(
        method='DELETE',
        url=url,
        params={'uuid': user_uuid}
    )

    assert status == HTTPStatus.UNAUTHORIZED
    assert body == 'Invalid access token'


@pytest.mark.asyncio
async def test_delete_wrong_uuid(login_user):
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<wrong_uuid>
    1) возвращается "Your access token doesn't permit request to this user"
    2) возвращается HTTPStatus.FORBIDDEN
    """
    body, _, _, _ = login_user
    url = USERS_URL + '/delete'
    wrong_uuid = str(uuid.uuid4())

    new_body, status = await get_response(
        method='DELETE',
        url=url,
        params={'uuid': wrong_uuid},
        cookies={'access_token': body['access_token']}
    )

    assert status == HTTPStatus.FORBIDDEN
    assert new_body == "Your access token doesn't permit request to this user"


@pytest.mark.asyncio
async def test_delete_correct(login_user):
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/users/delete?uuid=<uuid>
    с корректным access_cookie
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    body, user_uuid, _, _ = login_user
    url = USERS_URL + '/delete'

    new_body, status = await get_response(
        method='DELETE',
        url=url,
        params={'uuid': user_uuid},
        cookies={'access_token': body['access_token']}
    )

    assert status == HTTPStatus.OK
    assert new_body == "success"


@pytest.mark.asyncio
async def test_tokens_refresh_no_refresh():
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/refresh
    без refresh_token
    1) возвращается "Invalid refresh token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/refresh'

    body, status = await get_response(
        method='POST',
        url=url
    )

    assert status == HTTPStatus.UNAUTHORIZED
    assert body == 'Invalid refresh token'


@pytest.mark.asyncio
async def test_tokens_refresh_correct(login_user):
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
    body, _, _, _ = login_user
    url = USERS_URL + '/refresh'
    cookies = {'refresh_token': body['refresh_token']}

    body, status = await get_response(
        method='POST',
        url=url,
        cookies=cookies
    )

    assert status == HTTPStatus.OK
    assert isinstance(body, dict)
    assert 'refresh_token' in body
    assert 'access_token' in body
    assert isinstance(body['refresh_token'], str)
    assert isinstance(body['access_token'], str)


@pytest.mark.asyncio
async def test_history_no_access():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/history
    без access_token_cookie
    1) возвращается "Invalid access token"
    2) возвращается HTTPStatus.UNAUTHORIZED
    """
    url = USERS_URL + '/history'

    body, status = await get_response(
        method='GET',
        url=url
    )

    assert status == HTTPStatus.UNAUTHORIZED
    assert body == 'Invalid access token'


@pytest.mark.asyncio
async def test_history_correct_access(login_user):
    """
    Тест проверяет, что на запрос
    GET /auth/v1/users/history
    с корректным access_token_cookie
    1) возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
     [
         {
          "token_id": "uuid",
          "created_at": "str",
          "active_till": int,
          "user_id": "uuid"
         },
         ...
     ]
    3) возвращается HTTPStatus.OK
    """
    body, _, _, _ = login_user
    url = USERS_URL + '/history'
    cookies = {'access_token': body['access_token']}

    body, status = await get_response(
        method='GET',
        url=url,
        cookies=cookies
    )

    results = body['results']
    item = results[0]

    assert status == HTTPStatus.OK
    check_pagination(body)
    assert isinstance(results, list)
    assert isinstance(item, dict)
    assert 'token_id' in item
    assert 'created_at' in item
    assert 'active_till' in item
    assert 'user_id' in item
    assert isinstance(item['token_id'], str)
    assert isinstance(item['created_at'], str)
    assert isinstance(item['active_till'], int)
    assert isinstance(item['user_id'], str)


@pytest.mark.asyncio
async def test_logout_correct_access(login_user):
    """
    Тест проверяет, что на запрос
    POST /auth/v1/users/logout
    с корректным access_token_cookie
    1) возвращается "Logout successfully"
    2) возвращается HTTPStatus.OK
    """
    body, _, _, _ = login_user
    url = USERS_URL + '/logout'

    response_body, status = await get_response(
        method='POST',
        url=url,
        cookies={'access_token': body['access_token']}
    )

    assert status == HTTPStatus.OK
    assert response_body == "Logout successfully"
