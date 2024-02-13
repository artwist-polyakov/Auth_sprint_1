import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from configs.settings import Settings
from core.logger import LOGGING
from utils.creator_provider import get_creator

settings = Settings()
creator = get_creator()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)


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
