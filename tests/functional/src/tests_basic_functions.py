import aiohttp


async def get_response(url: str, params: dict):
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
