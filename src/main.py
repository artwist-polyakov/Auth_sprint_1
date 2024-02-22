import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.v1 import films, genres, persons, users
from configs.rbac_conf import RBAC_CONF, EXСLUDED_PATHS
from configs.settings import Settings
from core.logger import LOGGING
from db.auth.refresh_token import RefreshToken
from db.auth.role import Role
from db.auth.user import User
from db.postgres import PostgresProvider
from utils.creator_provider import get_creator
from utils.jwt_toolkit import dict_from_jwt

settings = Settings()
creator = get_creator()
postgres = PostgresProvider()


def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'delete',
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
        logging.warning(f"Resource: {resource}, Action: {action}")
        token = request.cookies.get("access_token")
        role = 'unauthorized'
        if token:
            role = dict_from_jwt(token).get('role', None)
            logging.warning(f"Role: {dict_from_jwt(token)}")
        else:
            refresh_token = request.cookies.get("refresh_token")
            if refresh_token:
                raise HTTPException(status_code=401, detail="Access token expired")
        if not role:
            raise HTTPException(status_code=401, detail="Bad credentials")
        if not resource in EXСLUDED_PATHS:
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


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

app.add_middleware(RBACMiddleware)


@app.on_event('startup')
async def startup():
    await postgres.create_schema(schema_name=settings.postgres_schema_2)
    await postgres.create_database(model=User)
    await postgres.create_database(model=Role)
    await postgres.create_database(model=RefreshToken)


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await creator.get_cache_storage().close()
    await creator.get_search_storage().close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix='/api/v1/films', tags=['Films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['Genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['Persons'])
app.include_router(users.router, prefix='/api/v1/users', tags=['Users'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.get_logging_level(),
    )
