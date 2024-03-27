from typing import Type

from db.models.search_requests.base_request import BaseRequest
from db.models.search_requests.films.search_all_films_request import (
    SearchAllFilmsRequest,
)
from db.models.search_requests.films.search_film_request import SearchFilmRequest
from db.models.search_requests.films.single_film_request import SingleFilmRequest
from db.models.search_requests.genres.all_genres_request import AllGenresRequest
from db.models.search_requests.genres.single_genre_request import SingleGenreRequest
from db.models.search_requests.persons.all_persons_request import AllPersonsRequest
from db.models.search_requests.persons.films_by_person_request import (
    FilmsByPersonRequest,
)
from db.models.search_requests.persons.list_of_films_by_person_request import (
    ListOfFilmsByPersonRequest,
)
from db.models.search_requests.persons.search_person_request import SearchPersonRequest
from db.models.search_requests.persons.single_person_request import SinglePersonRequest
from db.models.search_responses.base_response import BaseResponse
from db.models.search_responses.films.film_result import FilmResult
from db.models.search_responses.genres.genre_result import GenreResult
from db.models.search_responses.paginated_result import PaginatedResult
from db.models.search_responses.persons.film_role_result import (
    FilmRoleResult,
    ListFilmRoleResult,
)
from db.models.search_responses.persons.films_brief_result import (
    FilmBriefResult,
    ListFilmBriefResult,
)
from db.models.search_responses.persons.person_work_result import PersonWorkResult
from db.search.search_converter import SearchConverter


class ElasticConverter(SearchConverter):
    def map(self, data: dict, request_type: BaseRequest) -> BaseResponse:
        match request_type:
            case SingleFilmRequest():
                return self._convert_film_to_film_result(data)
            case SearchFilmRequest() | SearchAllFilmsRequest():
                return self._parse_any_paginated_result(data, request_type, FilmResult)
            case SingleGenreRequest():
                return self._convert_genre_to_genre_result(data)
            case AllGenresRequest():
                return self._parse_any_paginated_result(data, request_type, GenreResult)
            case FilmsByPersonRequest():
                return self._parse_films_by_person_result(data, request_type)
            case ListOfFilmsByPersonRequest():
                return self._parse_list_film_brief_result(data)
            case SearchPersonRequest() | AllPersonsRequest():
                return self._parse_any_paginated_result(data, request_type, PersonWorkResult)
            case SinglePersonRequest():
                return self._convert_person_to_person_result(data)
            case _:
                return BaseResponse()

    @staticmethod
    def _convert_film_to_film_result(data: dict) -> FilmResult:
        return FilmResult(**data['_source'])

    @staticmethod
    def _convert_genre_to_genre_result(data: dict) -> GenreResult:
        return GenreResult(**data['_source'])

    @staticmethod
    def _convert_person_to_person_result(data: dict) -> PersonWorkResult:
        return PersonWorkResult(**data['_source'])

    @staticmethod
    def _parse_list_film_brief_result(data: dict) -> ListFilmBriefResult:
        return ListFilmBriefResult(
            results=[FilmBriefResult(**hit['_source']) for hit in data['hits']['hits']]
        )

    @staticmethod
    def _parse_films_by_person_result(data: dict, request: BaseRequest) -> ListFilmRoleResult:
        films_data = []
        for hit in data['hits']['hits']:
            roles = []
            actors_ids = [actor['id'] for actor in hit['_source']['actors']]
            writers_ids = [writer['id'] for writer in hit['_source']['writers']]
            directors_ids = [director['id'] for director in hit['_source']['directors']]
            if request.person_id in actors_ids:
                roles.append('actor')

            if request.person_id in writers_ids:
                roles.append('writer')

            if request.person_id in directors_ids:
                roles.append('director')

            films_data.append(
                FilmRoleResult(
                    id=hit['_source']['id'],
                    roles=roles
                )
            )
        return ListFilmRoleResult(films=films_data)

    @staticmethod
    def _parse_any_paginated_result(
            data: dict,
            request: BaseRequest,
            nested_type: Type[BaseResponse]
    ) -> PaginatedResult:
        hits = data['hits']

        # Считаем количество страниц
        total_hits = hits['total']['value']
        num_pages = total_hits // request.size + bool(total_hits % request.size)

        # Формируем результат
        results = PaginatedResult(
            total=total_hits,
            page=request.page,
            pages=num_pages,
            per_page=request.size,
            results=[nested_type(**hit['_source']) for hit in hits['hits']]
        )
        return results
