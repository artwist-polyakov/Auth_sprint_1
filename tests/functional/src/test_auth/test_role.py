import random
import uuid
from http import HTTPStatus

import pytest
from configs.test_settings import settings
from src.tests_basic_functions import get_pg_response, create_user

ROLES_URL = settings.auth_url + '/roles'

random_five_digit_number = random.randint(10000, 99999)
ROLE_NAME = f'master{random_five_digit_number}'
WRONG_UUID = uuid.uuid4()
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
    data = {'params': params}
    response = await get_pg_response(
        method='POST',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert isinstance(body, dict)
    assert 'uuid' in body
    assert isinstance(body['uuid'], str)

    global CORRECT_UUID
    CORRECT_UUID = body['uuid']


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
    response = await get_pg_response(
        method='GET',
        url=url
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
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
    data = {'params': params}
    response = await get_pg_response(
        method='PUT',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    body = response.json()
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
    data = {'params': params}
    response = await get_pg_response(
        method='PUT',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
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
    data = {'params': params}
    response = await get_pg_response(
        method='DELETE',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    body = response.json()
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
    data = {'params': params}
    response = await get_pg_response(
        method='DELETE',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
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
    data = {'params': params}
    response = await get_pg_response(
        method='PUT',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    body = response.json()
    assert body == 'User not found'


@pytest.mark.asyncio
async def test_change_role_correct():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/change_role?uuid=<user_uuid>&new_role=master
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    user_response: tuple = await create_user()
    user_uuid: str = user_response[0]
    url = ROLES_URL + '/change_role'
    params = {'uuid': user_uuid, 'new_role': 'master'}
    data = {'params': params}
    response = await get_pg_response(
        method='PUT',
        url=url,
        data=data
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body == 'success'
