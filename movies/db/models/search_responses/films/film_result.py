from dataclasses import field

from db.models.search_responses.base_response import BaseResponse
from db.models.search_responses.genres.genre_result import GenreResult
from db.models.search_responses.persons.person_result import PersonResult


class FilmResult(BaseResponse):
    id: str = field(default='')
    imdb_rating: float = field(default=0.0)
    genres: list[GenreResult] = field(default_factory=list)
    title: str = field(default='')
    description: str | None = field(default='')
    directors_names: list[str] = field(default_factory=list)
    actors_names: list[str] = field(default_factory=list)
    writers_names: list[str] = field(default_factory=list)
    actors: list[PersonResult] = field(default_factory=list)
    writers: list[PersonResult] = field(default_factory=list)
    directors: list[PersonResult] = field(default_factory=list)
