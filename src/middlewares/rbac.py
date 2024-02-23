import logging

from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from configs.rbac_conf import EXСLUDED_PATHS, RBAC_CONF
from utils.jwt_toolkit import dict_from_jwt


def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'DELETE': 'delete',
    }
    return method_permission_mapping.get(method.upper(), 'read')


# CHeck if permission granted or not
def has_permission(user_role, resource_name, required_permission):
    if user_role in RBAC_CONF and resource_name in RBAC_CONF[user_role]:
        return required_permission in RBAC_CONF[user_role][resource_name]
    return False


class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_method = str(request.method).upper()
        action = translate_method_to_action(request_method)
        resource = request.url.path[1:]
        if resource not in EXСLUDED_PATHS:
            logging.warning(f"Resource: {resource}, Action: {action}")
            token = request.cookies.get("access_token")
            role = 'unauthorized'
            if token:
                role = dict_from_jwt(token).get('role', None)
                logging.warning(f"Role: {dict_from_jwt(token)}")
            else:
                refresh_token = request.cookies.get("refresh_token")
                if refresh_token and not ('user' in resource):
                    raise HTTPException(status_code=401, detail="Access token expired")
            if not role:
                raise HTTPException(status_code=401, detail="Bad credentials")
            if role != 'unauthorized' and not has_permission(role, resource.split("/")[2], action):
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