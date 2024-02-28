import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from configs.test_settings import settings
from src.tests_basic_functions import create_user, get_response
from testdata.testdata_genres import genres_data
from testdata.testdata_movies import movies_data
from testdata.testdata_persons import persons_data


def get_es_bulk_query() -> tuple((list[str], list[str])):
    bulk_query: list[dict] = []

    data = {
        'movies': movies_data,
        'genres': genres_data,
        'persons': persons_data
    }

    for index, index_data in data.items():
        for row in index_data:
            doc = {'_index': index, '_id': row['id']}
            doc.update({'_source': row})
            bulk_query.append(doc)
    return bulk_query, list(data.keys())


@pytest.fixture(scope='session')
async def es_client():
    es_client = AsyncElasticsearch(
        hosts=[f"http://{settings.es_1_host}:{settings.elastic_port}"],
        verify_certs=False
    )
    yield es_client
    await es_client.close()


@pytest.fixture(scope='session')
async def es_write_data(es_client):
    bulk_query, index_names = get_es_bulk_query()
    updated, errors = await async_bulk(client=es_client, actions=bulk_query)
    if errors:
        raise Exception('Ошибка записи данных в Elasticsearch')
    for item in index_names:
        await es_client.indices.refresh(index=item)
    yield True


@pytest.fixture(scope='function')
async def login_user():
    body, status, email, password = await create_user()
    user_uuid = body['uuid']
    url_login = (f'{settings.auth_url}/users/login'
                 f'?email={email}&password={password}')
    body, status = await get_response(
        method='GET',
        url=url_login
    )
    return body, user_uuid, email, password
