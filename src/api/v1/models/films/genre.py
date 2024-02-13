from api.v1.models.output import Output


class Genre(Output):
    """Модель ответа API для жанра"""
    uuid: str
    name: str
    description: str | None = None
