import asyncio
import logging
import secrets

import aiohttp
from configs.settings import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


async def get_response(
        url: str,
        params: dict = None,
        method: str = 'GET',
        cookies: dict = None,
        headers: dict = None
):
    """
    Функция отправляет асинхронный запрос на сервер
    и возвращает ответ
    """
    request_id = secrets.token_hex(16)
    headers_x = {'X-Request-Id': request_id}
    async with aiohttp.ClientSession(
            cookies=cookies if cookies else None,
            headers=headers if headers else headers_x
    ) as session:
        async with session.request(
                method=method.lower(),
                url=url,
                params=params
        ) as response:
            logging.warning(f"response: {response}")
            body = await response.json()
            status = response.status
            return body, status


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            url_login = settings.auth_api_login_url
            body, _ = asyncio.run(get_response(
                method='GET',
                url=url_login,
                params={'email': username, 'password': password, 'user_device_type': 'web'}
            ))

            user = User.objects.get(email=username)

            url_check = settings.auth_api_check_perm
            body, _ = asyncio.run(get_response(
                method='GET',
                url=url_check,
                params={'uuid': str(user.uuid), 'resource': 'admin', 'verb': 'read'},
                cookies={'access_token': body['access_token']}
            ))

            if isinstance(body, bool) and body:
                return user
            elif body['permission']:
                return user
            return None

        except Exception:
            return None

    def get_user(self, user_uuid):
        try:
            return User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            return None
