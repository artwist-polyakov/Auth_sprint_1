from dataclasses import field

from db.models.search_responses.base_response import BaseResponse


class FilmRoleResult(BaseResponse):
    id: str = field(default='')
    roles: list[str] = field(default_factory=list)


class ListFilmRoleResult(BaseResponse):
    films: list[FilmRoleResult] = field(default_factory=list)
