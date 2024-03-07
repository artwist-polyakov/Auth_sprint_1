import uvicorn
from api.v1 import roles, users
from configs.settings import Settings
from core.logger import LOGGING
from db.postgres import PostgresInterface
from middlewares.logout_processor import CheckLogoutMiddleware
from middlewares.rbac import RBACMiddleware
from utils.creator_provider import get_creator
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

settings = Settings()
creator = get_creator()
postgres = PostgresInterface()


def configure_tracer() -> None:
    resource = Resource.create(attributes={
        "service.name": "auth-app",
        "custom.data": "custom_data",
    })
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.jaeger_host,
                agent_port=settings.jaeger_port,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


configure_tracer()

app = FastAPI(
    title="Auth Service",
    docs_url='/auth/openapi',
    openapi_url='/auth/openapi.json',
    default_response_class=ORJSONResponse
)

FastAPIInstrumentor.instrument_app(app)

app.add_middleware(RBACMiddleware)
app.add_middleware(CheckLogoutMiddleware)


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
