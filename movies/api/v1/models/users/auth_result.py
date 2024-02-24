from orjson import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class AuthResult(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Token(AuthResult):
    access_token: str
    refresh_token: str
    token_type: str


class ISValid(AuthResult):
    is_valid: bool
