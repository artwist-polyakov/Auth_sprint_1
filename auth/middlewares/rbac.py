import logging

from configs.rbac_conf import EXСLUDED_PATHS, RBAC_CONF, get_rbac_conf
from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.jwt_toolkit import dict_from_jwt

ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"
UNAUTHORIZED_ROLE = "unauthorized"
ROLE_KEY = "role"
LOGIN_HANDLE = "user"


def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'DELETE': 'delete',
    }
    return method_permission_mapping.get(method.upper(), 'read')


async def has_permission(user_role, resource_name, required_permission):

    logging.warning(f"RBAC_CONF: {RBAC_CONF}")
    logging.warning(f"DB_conf: {await get_rbac_conf()}")
    conf = await get_rbac_conf()
    if user_role in conf and resource_name in conf[user_role]:
        return required_permission in conf[user_role][resource_name]
    return False


class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_method = str(request.method).upper()
        action = translate_method_to_action(request_method)
        resource = request.url.path[1:]
        if resource not in EXСLUDED_PATHS:
            token = request.cookies.get(ACCESS_TOKEN_KEY)
            role = UNAUTHORIZED_ROLE
            is_superuser = False
            if token:
                jwt = dict_from_jwt(token)
                role = jwt.get(ROLE_KEY, None)
                is_superuser = jwt.get("is_superuser", None)
            else:
                refresh_token = request.cookies.get(REFRESH_TOKEN_KEY)
                if refresh_token and not (LOGIN_HANDLE in resource):
                    raise HTTPException(status_code=401, detail="Access token expired")
            if not role:
                raise HTTPException(status_code=401, detail="Bad credentials")
            if not is_superuser and role != UNAUTHORIZED_ROLE and not await has_permission(
                    role,
                    resource.split("/")[2],
                    action
            ):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            logging.warning(f"Role: {role}")
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
