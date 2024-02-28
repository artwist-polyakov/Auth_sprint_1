import random

import aiohttp

from configs.test_settings import settings


async def get_response(url: str, params: dict = None, method: str = 'GET', cookies: dict = None):
    """
    Функция отправляет асинхронный запрос на сервер
    и возвращает ответ
    """
    async with aiohttp.ClientSession(cookies=cookies if cookies else None) as session:
        async with session.request(method=method.lower(), url=url, params=params) as response:
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


async def create_user(email: str = '', password: str = 'Aa123') -> tuple:
    """
    Функция генерирует email и пароль,
    отправляет асинхронный запрос на регистрацию пользователя
    и возвращает uuid, status, email и пароль
    """
    if email == '':
        random_five_digit_number = random.randint(10000, 99999)
        email = f'starfish{random_five_digit_number}@mail.ru'

    url = f'{settings.auth_url}/users/sign_up'

    body, status = await get_response(
        method='POST',
        url=url,
        params={'email': email, 'password': password}
    )
    # user_uuid = str(body[0]['uuid'])
    # token_type = body[0]['token_type']
    return body, status, email, password
