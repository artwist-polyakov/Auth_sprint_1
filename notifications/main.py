import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

from api.v1 import notifications
from configs.settings import get_settings
from core.logger import LOGGING
from middlewares.logging_middleware import LoggingMiddleware
from service.tasks_service import get_tasks_service

settings = get_settings()


def configure_tracer() -> None:
    resource = Resource.create(attributes={
        "service.name": "notifications-app",
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
    title=settings.api_name,
    docs_url='/notifications/openapi',
    openapi_url='/notifications/openapi.json',
    default_response_class=ORJSONResponse
)

if settings.enable_tracing:
    FastAPIInstrumentor.instrument_app(app)

app.add_middleware(LoggingMiddleware)


@app.on_event('shutdown')
async def shutdown():
    get_tasks_service().close()


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    tracer = trace.get_tracer(__name__)
    span = tracer.start_span('http.notifications')
    span.set_attribute('http.notifications_request_id', request_id)
    span.end()
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': 'X-Request-Id is required'})
    return response


app.include_router(notifications.router, prefix='/notifications/v1/tasks', tags=['Notifications'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.get_logging_level(),
    )
