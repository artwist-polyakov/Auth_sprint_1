from api.v1.models.films.genre import Genre
from api.v1.models.output import Output


class Film(Output):
    """Модель ответа API для фильма"""
    uuid: str
    title: str
    imdb_rating: float | None = None
    genres: list[Genre] | None = None
