from functools import lru_cache, wraps

from jose import JWTError, jwt

from configs.settings import JWTSecuritySettings


@lru_cache()
def get_jwt_settings():
    return JWTSecuritySettings()


def encode_jwt():
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if result and isinstance(result, dict):
                return jwt.encode(
                    result,
                    get_jwt_settings().openssl_key,
                    algorithm=get_jwt_settings().algorithm
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
                    get_jwt_settings().openssl_key,
                    algorithms=[get_jwt_settings().algorithm]
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
