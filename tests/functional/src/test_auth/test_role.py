from http import HTTPStatus

import httpx
import pytest
from configs.test_settings import settings
from src.tests_basic_functions import get_pg_response

ROLES_URL = settings.auth_url + '/roles'


@pytest.mark.asyncio
async def test_roles_add(add_and_login_user):
    """
    Тест проверяет, что на запрос
    POST auth/v1/roles/add?verb=master&resource=films&role=read
    1) возвращается словарь вида
        {
          "uuid": "uuid"
        }
    2) возвращается HTTPStatus.CREATED
    """

    url = ROLES_URL + '/add/'
    params = {'verb': 'master', 'resource': 'films', 'role': 'read'}
    access_token = (await add_and_login_user)['access_token']

    response = await get_pg_response(
        method='POST',
        url=url,
        params=params,
        cookies={'access_token': access_token}
    )

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()

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
    url = ROLES_URL + '/all/'


@pytest.mark.asyncio
async def test_roles_update_wrong():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/update?uuid=<wrong_uuid>&verb=master&resource=person&role=read
    1) возвращается "Role not found"
    2) возвращается HTTPStatus.NOT_FOUND
    """
    url = ROLES_URL + '/update/'


@pytest.mark.asyncio
async def test_roles_update_correct():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/update?uuid=<uuid>&verb=master&resource=person&role=read
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = ROLES_URL + '/update/'


@pytest.mark.asyncio
async def test_roles_delete_wrong():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/roles/delete?uuid=<wrong_uuid>
    1) возвращается "Role not found"
    2) возвращается HTTPStatus.NOT_FOUND
    """
    url = ROLES_URL + '/delete/'


@pytest.mark.asyncio
async def test_roles_delete_correct():
    """
    Тест проверяет, что на запрос
    DELETE /auth/v1/roles/delete?uuid=<uuid>
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = ROLES_URL + '/delete/'


@pytest.mark.asyncio
async def test_change_role_wrong():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/change_role?uuid=<wrong_uuid>&new_role=mmmmmaster
    1) возвращается "User not found"
    2) возвращается HTTPStatus.NOT_FOUND
    """
    url = ROLES_URL + '/change_role/'


@pytest.mark.asyncio
async def test_change_role_correct():
    """
    Тест проверяет, что на запрос
    PUT /auth/v1/roles/change_role?uuid=<uuid>&new_role=mmmmmaster
    1) возвращается "success"
    2) возвращается HTTPStatus.OK
    """
    url = ROLES_URL + '/change_role/'
