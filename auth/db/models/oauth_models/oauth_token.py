from core.base_orjson_model import BaseORJSONModel


class OAuthToken(BaseORJSONModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
