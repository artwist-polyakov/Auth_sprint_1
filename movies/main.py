import sentry_sdk
import uvicorn
from api.v1 import films, genres, persons
from configs.settings import get_settings
from core.logger import LOGGING
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.rbac import RBACMiddleware
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from utils.creator_provider import get_creator

settings = get_settings()
creator = get_creator()


def configure_tracer() -> None:
    resource = Resource.create(attributes={
        "service.name": "movies-app",
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
    if settings.jaeger_logs_in_console:
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


if settings.enable_tracing:
    configure_tracer()

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    enable_tracing=settings.sentry_enable_tracing,
)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

if settings.enable_tracing:
    FastAPIInstrumentor.instrument_app(app)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RBACMiddleware)


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    tracer = trace.get_tracer(__name__)
    span = tracer.start_span('http.movies')
    span.set_attribute('http.movies_request_id', request_id)
    span.end()
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': 'X-Request-Id is required'})
    return response


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

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.get_logging_level(),
    )
