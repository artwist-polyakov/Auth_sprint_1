import base64
from functools import lru_cache

import aiohttp

from configs.settings import get_settings
from db.models.token_models.oauth_token import OAuthToken
from db.oauth.oauth_service import OAuthService


class YandexOAuthService(OAuthService):
    def __init__(self):
        self._settings = get_settings()
        self._client_id = self._settings.yandex_oauth_client_id
        self._client_secret = self._settings.yandex_oauth_client_secret
        self._credentials = f"{self._client_id}:{self._client_secret}"

    async def exchange_code(self, code: str) -> OAuthToken:
        encoded_credentials = base64.b64encode(self._credentials.encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code
        }
        return await self._recieve_tokens(data, headers)

    async def _recieve_tokens(self, data: dict, headers: dict) -> OAuthToken:
        url = self._settings.yandex_oauth_url
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    # Успешный обмен
                    tokens = await response.json()
                    return OAuthToken(**tokens)
                else:
                    raise Exception(f"Failed to exchange code: {response.content}")


@lru_cache
def get_yandex_oauth_service() -> YandexOAuthService:
    return YandexOAuthService()
