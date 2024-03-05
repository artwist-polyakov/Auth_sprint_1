import asyncio
import logging
from http import HTTPStatus

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
    async with aiohttp.ClientSession(
            cookies=cookies if cookies else None,
            headers=headers
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
    def authenticate(self, request, username=None, password=None, **kwars):
        try:
            url = settings.auth_api_login_url
            body, status = asyncio.run(get_response(
                method='GET',
                url=url,
                params={'email': username, 'password': password, 'user_device_type': 'web'}
            ))

            if status == HTTPStatus.OK:
                return User.objects.get(email=username)
            return None

        except Exception:
            return None

    def get_user(self, user_uuid):
        try:
            return User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            return None
