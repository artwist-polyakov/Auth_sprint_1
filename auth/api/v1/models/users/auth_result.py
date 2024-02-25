from core.base_orjson_model import BaseORJSONModel


class Token(BaseORJSONModel):
    access_token: str
    refresh_token: str
    token_type: str


class ISValid(BaseORJSONModel):
    is_valid: bool
