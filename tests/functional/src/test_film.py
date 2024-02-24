from http import HTTPStatus

import pytest
from configs.test_settings import settings
from src.tests_basic_functions import check_pagination, get_response


def check_films_data(doc):
    """
    Функция проверяет, удовлетворяет ли документ из .../films/... требованиям:
    1) каждый словарь содержит поля uuid типа uuid, title типа str,
    imdb_rating типа float
    :param doc: документ
    """
    assert isinstance(doc, dict), "Документ должен быть словарем"
    assert 'uuid' in doc, "'uuid' должен быть в документе"
    assert 'title' in doc, "'title' должен быть в документе"
    assert 'imdb_rating' in doc, "'imdb_rating' должен быть в документе"

    assert isinstance(doc['uuid'], str), "'uuid' должен быть string"
    assert isinstance(doc['title'], str), "'title' должен быть string"
    assert isinstance(doc['imdb_rating'], float), \
        "'imdb_rating' должен быть float"


@pytest.mark.asyncio
async def test_films_rating(es_write_data):
    """
    Тест проверяет, что:
    1) на запрос
    GET /api/v1/films?sort=-imdb_rating&page_size=50&page_number=1
    возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
    [
        {
            "uuid": "uuid",
            "title": "str",
            "imdb_rating": "float"
        },
        ...
    ]
    3) фильмы отсортированы по убыванию рейтинга
    """
    url = settings.service_url + '/films/'
    params = {'per_page': 10, 'page': 1, 'sort': '-imdb_rating'}
    body, status = await get_response(url, params)

    assert status == HTTPStatus.OK

    assert len(body['results']) == 6, "В movies testdata 6 документов"

    check_pagination(body)
    doc = body['results'][0]
    check_films_data(doc)

    assert (body['results'][0]['imdb_rating'] >
            body['results'][-1]['imdb_rating']), \
        "Фильмы должны быть отсортированы по убыванию рейтинга"


@pytest.mark.asyncio
async def test_search_films(es_write_data):
    """
    Тест проверяет, что:
    1) на запрос
    GET /api/v1/films/search?query=love&page_number=1&page_size=50
    возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
    [
        {
          "uuid": "uuid",
          "title": "str",
          "imdb_rating": "float"
        },
        ...
    ]
    3) результаты содержат query в title или description
    """

    url = settings.service_url + '/films/search/'
    params = {'query': 'love', 'per_page': 10, 'page': 1}
    body, status = await get_response(url, params)

    assert status == HTTPStatus.OK
    print(f'body: {body}')
    assert len(body['results']) == 3, "Должно быть найдено 3 документа"

    check_pagination(body)
    doc = body['results'][0]
    check_films_data(doc)


@pytest.mark.asyncio
async def test_film_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/films/<uuid:UUID>/
    возвращается ответ вида
    {
        "uuid": "uuid",
        "title": "str",
        "imdb_rating": "float",
        "description": "str",
        "genre": [
          { "uuid": "uuid", "name": "str" },
          ...
        ],
        "actors": [
          {
            "uuid": "uuid",
            "full_name": "str"
          },
          ...
        ],
        "writers": [
          {
            "uuid": "uuid",
            "full_name": "str"
          },
          ...
        ],
        "directors": [
          {
            "uuid": "uuid",
            "full_name": "str"
          },
          ...
        ],
    }
    """
    url = settings.service_url + '/films/8a3bf41b-1cb4-4c3f-9bf1-b31d513e2003'
    body, status = await get_response(url, {})

    assert status == HTTPStatus.OK

    # uuid, title, imdb_rating
    check_films_data(body)

    assert 'description' in body
    assert 'genre' in body
    assert 'actors' in body
    assert 'writers' in body
    assert 'directors' in body

    assert isinstance(body['description'], str)
    assert isinstance(body['genre'], list)
    assert isinstance(body['actors'], list)
    assert isinstance(body['writers'], list)
    assert isinstance(body['directors'], list)

    if body['actors']:
        assert isinstance(body['actors'][0], dict)
        assert 'uuid' in body['actors'][0]
        assert 'full_name' in body['actors'][0]

    if body['writers']:
        assert isinstance(body['writers'][0], dict)
        assert 'uuid' in body['writers'][0]
        assert 'full_name' in body['writers'][0]

    if body['directors']:
        assert isinstance(body['directors'][0], dict)
        assert 'uuid' in body['directors'][0]
        assert 'full_name' in body['directors'][0]


@pytest.mark.asyncio
async def test_wrong_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/films/<uuid:UUID>/,
    где uuid указывает на несуществующий документ,
    возвращается ошибка 404
    """
    url = settings.service_url + '/films/000'
    body, status = await get_response(url, {})
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_films_rating_genre(es_write_data):
    """
    Тест проверяет, что:
    1) на запрос
    GET /api/v1/films?sort=-imdb_rating&genres=<uuid:UUID>
    возвращаются поля, соответствующие пагинированному ответу;
    2) results имеет вид
    [
        {
            "uuid": "uuid",
            "title": "str",
            "imdb_rating": "float"
        },
        ...
    ]
    3) фильмы отсортированы по убыванию рейтинга;
    4) фильмы относятся к жанру Romance (таких фильмов 2)
    """

    url = settings.service_url + '/films/'
    params = {'sort': '-imdb_rating',
              'genres': 'a36c826b-b2b0-4e96-9f88-4b8e09c4b120',  # Romance
              'per_page': 10,
              'page': 1}

    body, status = await get_response(url, params)

    assert status == HTTPStatus.OK
    assert len(body['results']) == 2, "Должно быть найдено 2 документа"

    check_pagination(body)
    doc = body['results'][0]
    check_films_data(doc)

    assert (body['results'][0]['imdb_rating'] >
            body['results'][-1]['imdb_rating']), \
        "Фильмы должны быть отсортированы по убыванию рейтинга"


@pytest.mark.asyncio
async def test_wrong_genre_uuid(es_write_data):
    """
    Тест проверяет, что на запрос
    GET /api/v1/films?sort=-imdb_rating&genres=<uuid:UUID>,
    где uuid жанра указывает на несуществующий жанр,
    возвращается 0 документов
    """
    url = settings.service_url + '/films/'
    params = {'sort': '-imdb_rating',
              'genres': '000',
              'per_page': 10,
              'page': 1}
    body, status = await get_response(url, params)
    assert status == HTTPStatus.OK
    assert len(body['results']) == 0, "Нет документов в с таким uuid"

    check_pagination(body)
