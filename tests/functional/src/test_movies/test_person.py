from http import HTTPStatus

import pytest

from configs.test_settings import settings
from src.test_movies.test_film import check_films_data
from src.tests_basic_functions import check_pagination, get_response

MOVIES_URL = settings.movies_url


def check_person(doc):
    assert isinstance(doc, dict)
    assert 'uuid' in doc
    assert 'full_name' in doc
    assert 'films' in doc
    assert isinstance(doc['uuid'], str)
    assert isinstance(doc['full_name'], str)
    assert isinstance(doc['films'], list)

    # Проверка первого фильма в списке фильмов
    if doc['films'][0]:
        film = doc['films'][0]
        assert isinstance(film, dict)
        assert 'uuid' in film
        assert 'roles' in film
        assert isinstance(film['uuid'], str)
        assert isinstance(film['roles'], list)


@pytest.mark.asyncio
async def test_search_persons(es_write_data):
    """
    Тест проверяет, что:
    1) на запрос
    GET /api/v1/persons/search?query=writer&page_number=1&page_size=50
    возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
    [
        {
          "uuid": "uuid",
          "full_name": "str",
          "films": [
                  {
                    "uuid": "uuid",
                    "roles": ["str"]
                  },
                  ...
          ]
        },
        ...
    ]
    """

    url = MOVIES_URL + '/persons/search/'
    params = {'query': 'writer', 'per_page': 10, 'page': 1}
    body, status = await get_response(url, params)

    assert status == HTTPStatus.OK
    assert len(body['results']) == 3, "Должно быть найдено 3 документа"

    check_pagination(body)

    doc = body['results'][0]
    check_person(doc)


@pytest.mark.asyncio
async def test_person_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/persons/<uuid:UUID>
    возвращается ответ вида
    {
        "uuid": "uuid",
        "full_name": "str",
        "films": [
            {
              "uuid": "uuid",
              "roles": ["str"]
            },
            ...
        ]
    }
    """

    url = MOVIES_URL + '/persons/d1cf010d-5941-4877-a22b-c137a642370c'
    body, status = await get_response(url, {})

    assert status == HTTPStatus.OK
    check_person(body)


@pytest.mark.asyncio
async def test_person_uuid_film(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/persons/<uuid:UUID>/film
    возвращается ответ вида
    [
        {
          "uuid": "uuid",
          "title": "str",
          "imdb_rating": "float"
        },
        ...
    ]
    """
    url = (MOVIES_URL +
           '/persons/d1cf010d-5941-4877-a22b-c137a642370c/film')
    body, status = await get_response(url, {})

    assert status == HTTPStatus.OK
    assert len(body) == 1, "Должен быть 1 документ"
    check_films_data(body[0])


@pytest.mark.asyncio
async def test_person_wrong_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/persons/<uuid:UUID>/,
    где uuid указывает на несуществующий документ,
    возвращается ошибка 404
    """

    url = MOVIES_URL + '/persons/000'
    body, status = await get_response(url, {})
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_persons(es_write_data):
    """
    Тест проверяет, что:
    1) на запрос
    GET /persons/?page=1&per_page=10
    возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
    [
        {
            "uuid": "uuid",
            "full_name": "str"
        },
        ...
    ]
    """
    url = MOVIES_URL + '/persons/'
    params = {'per_page': 10, 'page': 1}
    body, status = await get_response(url, params)

    assert status == HTTPStatus.OK
    assert len(body['results']) == 10, "В persons testdata 10 документов"

    check_pagination(body)
    doc = body['results'][0]
    assert 'uuid' in doc
    assert 'full_name' in doc
    assert isinstance(doc['uuid'], str)
    assert isinstance(doc['full_name'], str)
