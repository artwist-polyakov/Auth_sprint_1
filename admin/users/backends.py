import asyncio
import logging
import secrets

import requests

from configs.settings import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


def get_response(
        url: str,
        params: dict = None,
        method: str = 'GET',
        cookies: dict = None,
        headers: dict = None
):
    """
    Функция отправляет синхронный запрос на сервер
    и возвращает ответ
    """
    request_id = secrets.token_hex(16)
    headers_x = {'X-Request-Id': request_id}

    with requests.Session() as session:
        response = session.request(
            method=method.upper(),
            url=url,
            params=params,
            cookies=cookies,
            headers=headers if headers else headers_x
        )
        logging.warning(f"response: {response}")
        body = response.json()
        status = response.status_code
        return body, status


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            url_login = settings.auth_api_login_url
            body, _ = get_response(
                method='GET',
                url=url_login,
                params={'email': username, 'password': password, 'user_device_type': 'web'}
            )

            user = User.objects.get(email=username)

            url_check = settings.auth_api_check_perm
            body, _ = get_response(
                method='GET',
                url=url_check,
                params={'uuid': str(user.uuid), 'resource': 'admin', 'verb': 'read'},
                cookies={'access_token': body['access_token']}
            )

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
