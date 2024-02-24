from db.models.token_models.access_token_container import AccessTokenContainer
from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.creator_provider import get_creator
from utils.jwt_toolkit import dict_from_jwt

ACCESS_TOKEN_KEY = "access_token"


class CheckLogoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get(ACCESS_TOKEN_KEY)
        resource = request.url.path[1:]
        if token and not ('login' in resource or 'sign_up' in resource):
            token = AccessTokenContainer(
                **dict_from_jwt(token)
            )
            if await get_creator().get_logout_storage().is_blacklisted(token):
                return ORJSONResponse(
                    status_code=401,
                    content="Token is logout, please re-login"
                )
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
