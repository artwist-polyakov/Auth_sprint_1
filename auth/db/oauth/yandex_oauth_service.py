import base64
from functools import lru_cache
from http import HTTPStatus

import aiohttp
from configs.settings import get_settings
from db.models.oauth_models.oauth_token import OAuthToken
from db.oauth.oauth_service import OAuthRepository


class YandexOAuthRepository(OAuthRepository):
    _YANDEX_LOGIN_URL = get_settings().yandex_login_url
    _YANDEX_REVOKE_TOKEN_URL = get_settings().yandex_revoke_token_url

    def __init__(self):
        self._settings = get_settings()
        self._client_id = self._settings.yandex_oauth_client_id
        self._client_secret = self._settings.yandex_oauth_client_secret
        self._credentials = f"{self._client_id}:{self._client_secret}"

    async def revoke_token(self, access_token: str) -> None:
        headers = self._get_secret_headers()
        data = {
            "access_token": access_token
        }
        url = self._YANDEX_REVOKE_TOKEN_URL
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status != HTTPStatus.OK:
                    self._raise_exception(response)
        return None

    async def get_user_info(self, token: str) -> dict:
        headers = self._get_token_headers(token)
        async with aiohttp.ClientSession() as session:
            async with session.get(self._YANDEX_LOGIN_URL, headers=headers) as response:
                if response.status == HTTPStatus.OK:
                    user_info = await response.json()
                    return user_info
                else:
                    self._raise_exception(response)

    async def refresh_token(self, refresh_token: str) -> OAuthToken:
        headers = self._get_secret_headers()
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        return await self._recieve_tokens(data, headers)

    async def exchange_code(self, code: str) -> OAuthToken:
        headers = self._get_secret_headers()
        data = {
            "grant_type": "authorization_code",
            "code": code
        }
        return await self._recieve_tokens(data, headers)

    async def _recieve_tokens(self, data: dict, headers: dict) -> OAuthToken:
        url = self._settings.yandex_oauth_url
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == HTTPStatus.OK:
                    # Успешный обмен
                    tokens = await response.json()
                    return OAuthToken(**tokens)
                else:
                    self._raise_exception(response)

    def _get_token_headers(self, token: str) -> dict:
        return {
            "Authorization": f"OAuth {token}"
        }

    def _get_secret_headers(self) -> dict:
        encoded_credentials = base64.b64encode(self._credentials.encode()).decode()
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }

    def _raise_exception(self, response: aiohttp.ClientResponse) -> None:
        raise Exception(f"Failed to exchange code: {response.status}")


@lru_cache
def get_yandex_oauth_rep() -> YandexOAuthRepository:
    return YandexOAuthRepository()
