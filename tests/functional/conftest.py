import random
from http import HTTPStatus
from http.client import HTTPException

import httpx

import pytest

from configs.test_settings import settings
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
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


@pytest.fixture(scope='module')
async def add_and_login_user():
    random_five_digit_number = random.randint(10000, 99999)
    email = f'starfish{random_five_digit_number}@mail.ru'
    password = 'Aa123'

    host_add = f'http://{settings.postgres_host}:{settings.postgres_port}/sign_up'
    host_login = f'http://{settings.postgres_host}:{settings.postgres_port}/login'

    async with httpx.AsyncClient(headers={"Content-Type": "application/json"}) as client:
        for host in [host_add, host_login]:
            response = await client.post(
                url=host,
                data={'email': email, 'password': password},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code != HTTPStatus.CREATED or HTTPStatus.OK:
                raise Exception('Ошибка sign up & login')

    parsed_response = response.json()
    return parsed_response
