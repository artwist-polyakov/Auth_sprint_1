import uvicorn
from configs.settings import Settings
from core.logger import LOGGING
from db.auth.refresh_token import RefreshToken
from db.auth.role import Role
from db.auth.user import User
from db.postgres import PostgresProvider
from db.roles.default_roles import default_roles
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from middlewares.logout_processor import CheckLogoutMiddleware
from middlewares.rbac import RBACMiddleware
from utils.creator_provider import get_creator

from api.v1 import roles, users

settings = Settings()
creator = get_creator()
postgres = PostgresProvider()

app = FastAPI(
    title='Auth Service',
    docs_url='/auth/openapi',
    openapi_url='/auth/openapi.json',
    default_response_class=ORJSONResponse
)

app.add_middleware(RBACMiddleware)
app.add_middleware(CheckLogoutMiddleware)


@app.on_event('startup')
async def startup():
    await postgres.create_schema(schema_name=settings.postgres_schema_2)
    await postgres.create_database(model=User)
    await postgres.create_database(model=Role)
    await postgres.create_database(model=RefreshToken)
    await postgres.load_default_roles(default_roles=default_roles)


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await creator.get_cache_storage().close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(users.router, prefix='/auth/v1/users', tags=['Users'])
app.include_router(roles.router, prefix='/auth/v1/roles', tags=['Roles'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.get_logging_level(),
    )
