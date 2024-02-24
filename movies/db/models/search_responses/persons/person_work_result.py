from dataclasses import field

from db.models.search_responses.base_response import BaseResponse
from db.models.search_responses.persons.film_role_result import FilmRoleResult


class PersonWorkResult(BaseResponse):
    id: str = field(default='')
    full_name: str = field(default='')
    films: list[FilmRoleResult] = field(default_factory=list)
