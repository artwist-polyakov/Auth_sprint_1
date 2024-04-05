from functools import wraps

from jose import JWTError, jwt

from core.settings import settings


def encode_jwt():
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if result and isinstance(result, dict):
                return jwt.encode(
                    result,
                    settings.token.openssl_key,
                    algorithm=settings.token.algorithm
                )
            else:
                return result

        return inner

    return wrapper


def decode_jwt():
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                token = func(*args, **kwargs)
                return jwt.decode(
                    token,
                    settings.token.openssl_key,
                    algorithms=[settings.token.algorithm]
                )
            except JWTError:
                return {}

        return inner

    return wrapper


@encode_jwt()
def dict_to_jwt(data: dict) -> dict | str:
    return data


@decode_jwt()
def dict_from_jwt(data: str) -> str | dict:
    return data
