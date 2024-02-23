from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from db.models.token_models.access_token_container import AccessTokenContainer
from utils.creator_provider import get_creator
from utils.jwt_toolkit import dict_from_jwt

ACCESS_TOKEN_KEY = "access_token"


class CheckLogoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get(ACCESS_TOKEN_KEY)
        if token:
            token = AccessTokenContainer(
                **dict_from_jwt(token)
            )
            if await get_creator().get_logout_storage().is_blacklisted(token):
                raise HTTPException(status_code=401, detail="Token is logout")
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )