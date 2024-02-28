import random

import aiohttp
import httpx

from configs.test_settings import settings


async def get_es_response(url: str, params: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            body = await response.json()
            status = response.status
            return body, status


def check_pagination(data):
    """
    Функция проверяет, удовлетворяет ли ответ на запрос требованиям:
    1) ответ содержит поля total, pages, page, per_page, results;
    2) results является списком словарей
    :param data: ответ на запрос
    """
    assert 'total' in data, "'total' должен быть в ответе"
    assert 'pages' in data, "'pages' должен быть в ответе"
    assert 'page' in data, "'page' должен быть в ответе"
    assert 'per_page' in data, "'per_page' должен быть в ответе"
    assert 'results' in data, "'results' должен быть в ответе"

    assert isinstance(data['results'], list), \
        "data['results'] должен быть list"


async def get_pg_response(method: str, url: str, data=None):
    async with httpx.AsyncClient() as client:
        if data:
            response = await getattr(client, method.lower())(url=url, **data)
        else:
            response = await getattr(client, method.lower())(url=url)
    return response


async def create_user() -> tuple:
    random_five_digit_number = random.randint(10000, 99999)
    email = f'starfish{random_five_digit_number}@mail.ru'
    password = 'Aa123'

    url = f'{settings.auth_url}/users/sign_up'

    response = await get_pg_response(
        method='POST',
        url=url,
        data={'params': {'email': email, 'password': password}}
    )
    uuid = response.json()['uuid']
    return uuid, email, password
