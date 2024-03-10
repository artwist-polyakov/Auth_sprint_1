from http import HTTPStatus

from configs.settings import get_settings
from db.rate_limiter.redis_rate_limiter import get_rate_limiter
from fastapi import Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.jwt_toolkit import dict_from_jwt

ACCESS_TOKEN_KEY = "access_token"
USER_ID_KEY = "user_id"
REQUEST_ID_KEY = "X-Request-Id"
MAX_REQUESTS_PER_MINUTE = get_settings().requests_rate_limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        key = 'some_key'  # на случай, если не будет токена и не будет хоста
        if token := request.cookies.get(ACCESS_TOKEN_KEY):
            jwt = dict_from_jwt(token)
            key = jwt.get(USER_ID_KEY, str(request.client.host))
        else:
            key = str(request.client.host)
        if not await get_rate_limiter().is_within_limit(key, MAX_REQUESTS_PER_MINUTE):
            return ORJSONResponse(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                content="Too Many Requests"
            )
        request_id = request.headers.get(REQUEST_ID_KEY, "1")
        await get_rate_limiter().add_request(key, request_id)
        response = await call_next(request)
        return response
