import logging
from fastapi.responses import ORJSONResponse
import aiohttp
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
from http import HTTPStatus

from utils.jwt_toolkit import dict_from_jwt

ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"
UNAUTHORIZED_ROLE = "unauthorized"
ROLE_KEY = "role"

# todo настроить EXСLUDED_PATHS через окружение
EXСLUDED_PATHS = ['docs', 'openapi.json', 'api/openapi', 'api/openapi.json']


def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'DELETE': 'delete',
    }
    return method_permission_mapping.get(method.upper(), 'read')


async def get_response(url: str, params: dict = None, method: str = 'GET', cookies: dict = None):
    """
    Функция отправляет асинхронный запрос на сервер
    и возвращает ответ
    """
    async with aiohttp.ClientSession(cookies=cookies if cookies else None) as session:
        async with session.request(method=method.lower(), url=url, params=params) as response:
            body = await response.json()
            status = response.status
            return body, status


async def has_permission(user_role, resource_name, required_permission):
    url = 'http://auth:8000/auth/v1/users/check_permissions/'
    params = {
        'role': user_role,
        'resource': resource_name,
        'verb': required_permission
    }
    logging.warning(f"params: {params}")
    result, status = await get_response(url=url, params=params)
    logging.warning(f"result: {result}")
    logging.warning(f"status: {status}")
    if status == HTTPStatus.OK:
        return result.get('permission', False)
    return False


class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_method = str(request.method).upper()
        action = translate_method_to_action(request_method)
        resource = request.url.path[1:]
        logging.warning(f"resource: {resource}")
        if resource not in EXСLUDED_PATHS:
            token = request.cookies.get(ACCESS_TOKEN_KEY)
            role = UNAUTHORIZED_ROLE
            is_superuser = False
            logging.warning(f"token: {token}")
            if token:
                logging.warning('token exists')
                jwt = dict_from_jwt(token)
                logging.warning(f"jwt: {jwt}")
                role = jwt.get(ROLE_KEY, None)
                logging.warning(f"role: {role}")
                is_superuser = jwt.get("is_superuser", None)
                logging.warning(f"is_superuser: {is_superuser}")
            logging.warning(f"role: {role}")
            if not role:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Bad credentials")
            if not is_superuser and not await has_permission(role, resource.split("/")[2], action):
                return ORJSONResponse(
                    status_code=HTTPStatus.FORBIDDEN,
                    content="Permission denied")
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
