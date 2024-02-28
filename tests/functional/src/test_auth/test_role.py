import random
import uuid
from http import HTTPStatus

import pytest
from configs.test_settings import settings
from src.tests_basic_functions import create_user, get_response

ROLES_URL = settings.auth_url + '/roles'

random_five_digit_number = random.randint(10000, 99999)
ROLE_NAME = f'master{random_five_digit_number}'
WRONG_UUID = str(uuid.uuid4())
CORRECT_UUID = str()


@pytest.mark.asyncio
async def test_roles_add():
    """
    Тест проверяет, что на запрос
    POST auth/v1/roles/add?role=master&resource=films&verb=read
    1) возвращается словарь вида
        {
          "uuid": "uuid"
        }
    2) возвращается HTTPStatus.CREATED
    """

    url = ROLES_URL + '/add'
    params = {'role': ROLE_NAME, 'resource': 'films', 'verb': 'read'}
    body, status = await get_response(
        method='POST',
        url=url,
        params=params
    )

    global CORRECT_UUID
    CORRECT_UUID = body['uuid']

    assert status == HTTPStatus.CREATED
    assert isinstance(body, dict)
    assert 'uuid' in body
    assert isinstance(body['uuid'], str)


@pytest.mark.asyncio
async def test_roles_all():
    """
    Тест проверяет, что на запрос
    GET /auth/v1/roles/all
    1) возвращается словарь вида
        {
          "admin": {
            "films": [
              "read",
              "write",
              "delete"
            ],
            ...
          },
          ...
        }
    2) возвращается HTTPStatus.OK
    """
    url = ROLES_URL + '/all'
    body, status = await get_response(
        method='GET',
        url=url
    )

    assert status == HTTPStatus.OK
    assert isinstance(body, dict)
    assert isinstance(body[ROLE_NAME], dict)
    assert isinstance(body[ROLE_NAME]['films'], list)


@pytest.mark.asyncio
async def test_roles_update_wrong():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/update?uuid=<wrong_uuid>&role=master2&resource=films2&verb=read2
    1) возвращается "Role not found"
    2) возвращается HTTPStatus.NOT_FOUND
    """
    url = ROLES_URL + '/update'
    params = {'uuid': WRONG_UUID, 'role': f'{ROLE_NAME}2', 'resource': 'films2', 'verb': 'read2'}
    body, status = await get_response(
        method='PUT',
        url=url,
        params=params
    )

    assert status == HTTPStatus.NOT_FOUND
    assert body == 'Role not found'


@pytest.mark.asyncio
async def test_roles_update_correct():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/update?uuid=<uuid>&verb=master&resource=person&role=read
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = ROLES_URL + '/update'
    params = {'uuid': CORRECT_UUID, 'role': f'{ROLE_NAME}2', 'resource': 'films2', 'verb': 'read2'}
    body, status = await get_response(
        method='PUT',
        url=url,
        params=params
    )

    assert status == HTTPStatus.OK
    assert body == 'success'


@pytest.mark.asyncio
async def test_roles_delete_wrong():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/roles/delete?uuid=<wrong_uuid>
    1) возвращается "role not found"
    2) возвращается HTTPStatus.NOT_FOUND
    """
    url = ROLES_URL + '/delete'
    params = {'uuid': WRONG_UUID}
    body, status = await get_response(
        method='DELETE',
        url=url,
        params=params
    )

    assert status == HTTPStatus.NOT_FOUND
    assert body == 'role not found'


@pytest.mark.asyncio
async def test_roles_delete_correct():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/roles/delete?uuid=<uuid>
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = ROLES_URL + '/delete'
    params = {'uuid': CORRECT_UUID}
    body, status = await get_response(
        method='DELETE',
        url=url,
        params=params
    )

    assert status == HTTPStatus.OK
    assert body == 'success'


@pytest.mark.asyncio
async def test_change_role_wrong():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/change_role?uuid=<wrong_user_uuid>&new_role=master
    1) возвращается "User not found"
    2) возвращается HTTPStatus.NOT_FOUND
    """
    url = ROLES_URL + '/change_role'
    params = {'uuid': WRONG_UUID, 'new_role': 'master'}
    body, status = await get_response(
        method='PUT',
        url=url,
        params=params
    )

    assert status == HTTPStatus.NOT_FOUND
    assert body == 'User not found'


@pytest.mark.asyncio
async def test_change_role_correct():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/change_role?uuid=<user_uuid>&new_role=master
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    body, *args = await create_user()
    user_uuid = body['uuid']
    url = ROLES_URL + '/change_role'
    params = {'uuid': str(user_uuid), 'new_role': 'master'}
    body, status = await get_response(
        method='PUT',
        url=url,
        params=params
    )

    assert status == HTTPStatus.OK
    assert body == 'success'
