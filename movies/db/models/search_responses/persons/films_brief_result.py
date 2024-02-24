from dataclasses import field

from db.models.search_responses.base_response import BaseResponse


class FilmBriefResult(BaseResponse):
    id: str = field(default='')
    title: str = field(default='')
    imdb_rating: float = field(default=0.0)


class ListFilmBriefResult(BaseResponse):
    results: list[FilmBriefResult] = field(default_factory=list)
