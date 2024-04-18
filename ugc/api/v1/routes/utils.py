import jwt
from core.settings import settings


class InvalidTokenError(Exception):
    pass


class NoTokenError(Exception):
    pass


def _get_token_from_cookie(request_container) -> str:
    access_token_cookie = request_container.cookies.get("access_token")
    if not access_token_cookie:
        raise NoTokenError("Access token not found")
    try:
        decoded_token = jwt.decode(
            access_token_cookie,
            settings.token.openssl_key,
            algorithms=[settings.token.algorithm],
        )
        return decoded_token["user_id"]
    except Exception:
        raise InvalidTokenError("Invalid token")
