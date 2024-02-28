from http import HTTPStatus

import pytest
from configs.test_settings import settings
from src.tests_basic_functions import check_pagination, get_response


MOVIES_URL = settings.movies_url


@pytest.mark.asyncio
async def test_genres(es_write_data):
    """
    Тест проверяет, что:
    1) на запрос
    GET /api/v1/genres/
    возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
    [
        {
          "uuid": "uuid",
          "name": "str",
          ...
        },
        ...
    ]
    """
    url = MOVIES_URL + '/genres/'
    params = {'per_page': 10, 'page': 1}
    body, status = await get_response(url, params)

    assert status == HTTPStatus.OK
    assert len(body['results']) == 7, "В genres testdata 7 документов"

    check_pagination(body)
    doc = body['results'][0]
    assert 'uuid' in doc
    assert 'name' in doc
    assert isinstance(doc['uuid'], str)
    assert isinstance(doc['name'], str)


@pytest.mark.asyncio
async def test_genre_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/genres/<uuid:UUID>
    возвращается ответ вида
    {
    "uuid": "uuid",
    "name": "str",
    "description": "str"
    }
    """
    url = MOVIES_URL + '/genres/69717732-0b46-4290-8727-7a5db7d1ea9d'
    doc, status = await get_response(url, {})

    assert status == HTTPStatus.OK

    assert 'uuid' in doc
    assert 'name' in doc
    assert 'description' in doc
    assert isinstance(doc['uuid'], str)
    assert isinstance(doc['name'], str)
    assert isinstance(doc['description'], str)


@pytest.mark.asyncio
async def test_genre_wrong_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/genres/<uuid:UUID>/,
    где uuid указывает на несуществующий документ,
    возвращается ошибка 404
    """
    url = MOVIES_URL + '/genres/000'
    body, status = await get_response(url, {})
    assert status == HTTPStatus.NOT_FOUND
