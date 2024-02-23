from api.v1.models.films.genre import Genre
from api.v1.models.films.person import Person
from api.v1.models.output import Output


class DetailedFilm(Output):
    """Модель ответа API для фильма"""
    uuid: str
    title: str
    imdb_rating: float | None = None
    description: str | None = None
    genre: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []
