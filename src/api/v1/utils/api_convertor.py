from api.v1.models.films.detailed_film import DetailedFilm
from api.v1.models.films.film import Film
from api.v1.models.films.genre import Genre
from api.v1.models.films.person import Person
from api.v1.models.genres.detailed_genre import DetailedGenre
from api.v1.models.paginated_output import PaginatedOutput
from api.v1.models.persons.film_brief import FilmBrief
from api.v1.models.persons.person_films import PersonFilms
from api.v1.models.persons.work_record import WorkRecord
from db.models.search_responses.base_response import BaseResponse
from db.models.search_responses.films.film_result import FilmResult
from db.models.search_responses.genres.genre_result import GenreResult
from db.models.search_responses.paginated_result import PaginatedResult
from db.models.search_responses.persons.films_brief_result import \
    ListFilmBriefResult
from db.models.search_responses.persons.person_work_result import \
    PersonWorkResult
from db.models.token_models.access_token_container import AccessTokenContainer
from utils.jwt_toolkit import dict_to_jwt, get_jwt_settings, dict_from_jwt


class APIConvertor:

    def map_films(
            self,
            response_type: BaseResponse,
            params: str = 'default'
    ) -> DetailedFilm | PaginatedOutput[Film]:
        if (isinstance(response_type, PaginatedResult)
                and ((response_type.results
                      and isinstance(response_type.results[0], FilmResult))
                     or response_type.results == [])):
            return self._parse_films(response_type, params)
        elif isinstance(response_type, FilmResult):
            return self._parse_film(response_type, params)
        else:
            raise ValueError(f"Invalid response type: {response_type}")

    def map_genres(
            self,
            response: BaseResponse,
            params: str = 'default'
    ) -> DetailedGenre | PaginatedOutput[Genre]:
        if isinstance(
                response,
                GenreResult
        ):
            return self._parse_genre(response, params)
        elif (isinstance(response, PaginatedResult)
              and ((response.results
                    and isinstance(response.results[0], GenreResult))
                   or response.results == [])):
            return self._parse_genres(response, params)
        else:
            raise ValueError(f"Invalid response type: {response}")

    def map_persons(
            self,
            response: BaseResponse,
            params: str = 'default'
    ) -> PaginatedOutput[PersonFilms] | PaginatedOutput[Person] | list[FilmBrief] | PersonFilms:
        if (isinstance(response, PaginatedResult)
                and ((response.results
                      and isinstance(response.results[0], PersonWorkResult))
                     or response.results == [])):
            return self._parse_persons(response, params)
        elif isinstance(response, ListFilmBriefResult):
            return self._parse_person_participation(response, params)
        elif isinstance(response, PersonWorkResult):
            return self._parse_person_work_result(response, params)
        else:
            raise ValueError(f"Invalid response type: {response}")

    @staticmethod
    def _parse_films(films: PaginatedResult[FilmResult], params: str) -> PaginatedOutput[Film]:
        if films.total == 0:
            return PaginatedOutput[Film](total=0, page=1, pages=0, per_page=films.per_page,
                                         results=[])
        result = [Film(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating if film.imdb_rating else None,
            genres=[Genre(uuid=genre.id, name=genre.name, description=genre.description)
                    for genre in film.genres] if film.genres else None,
        ) for film in
            films.results]
        return PaginatedOutput[Film](total=films.total, page=films.page, pages=films.pages,
                                     per_page=films.per_page, results=result)

    @staticmethod
    def _parse_film(film: FilmResult, params: str) -> DetailedFilm:
        return DetailedFilm(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating if film.imdb_rating else None,
            description=film.description if film.description else '',
            genre=[Genre(uuid=genre.id, name=genre.name, description=genre.description)
                   for genre in film.genres],
            actors=[Person(uuid=actor.id, full_name=actor.name) for actor in film.actors],
            writers=[Person(uuid=writer.id, full_name=writer.name) for writer in film.writers],
            directors=[Person(uuid=director.id, full_name=director.name)
                       for director in film.directors]
        )

    @staticmethod
    def _parse_genre(genre: GenreResult, params: str) -> DetailedGenre:
        return DetailedGenre(
            uuid=genre.id,
            name=genre.name,
            description=genre.description if genre.description else ''
        )

    @staticmethod
    def _parse_genres(genres: PaginatedResult[GenreResult], params: str) -> PaginatedOutput[Genre]:
        if genres.total == 0:
            return PaginatedOutput[Genre](total=0, page=1, pages=0, per_page=genres.per_page,
                                          results=[])
        result = [Genre(
            uuid=genre.id,
            name=genre.name,
            description=genre.description if genre.description else ''
        ) for genre in
            genres.results]
        return PaginatedOutput[Genre](total=genres.total, page=genres.page, pages=genres.pages,
                                      per_page=genres.per_page, results=result)

    @staticmethod
    def _parse_person_work_result(
            person: PersonWorkResult,
            params: str = 'default'
    ) -> PersonFilms | Person:
        if params == 'brief':
            return Person(
                uuid=person.id,
                full_name=person.full_name
            )
        else:
            return PersonFilms(
                uuid=person.id,
                full_name=person.full_name,
                films=[WorkRecord(
                    uuid=film.id,
                    roles=film.roles
                ) for film in person.films]
            )

    @staticmethod
    def _parse_persons(
            persons: PaginatedResult[PersonWorkResult],
            params: str = 'default'
    ) -> PaginatedOutput[PersonFilms] | PaginatedOutput[Person]:
        if persons.total == 0:
            return PaginatedOutput[PersonFilms](
                total=0,
                page=1,
                pages=0,
                per_page=persons.per_page,
                results=[]
            )
        result = [APIConvertor._parse_person_work_result(person, params) for person in
                  persons.results]
        if params == 'brief':
            return PaginatedOutput[Person](
                total=persons.total,
                page=persons.page,
                pages=persons.pages,
                per_page=persons.per_page,
                results=result)
        else:
            return PaginatedOutput[PersonFilms](
                total=persons.total,
                page=persons.page,
                pages=persons.pages,
                per_page=persons.per_page,
                results=result)

    @staticmethod
    def _parse_person_participation(films: ListFilmBriefResult, params: str) -> list[FilmBrief]:
        return [
            FilmBrief(
                uuid=film.id,
                title=film.title,
                imdb_rating=film.imdb_rating if film.imdb_rating else None
            ) for film in films.results
        ]

    @staticmethod
    def map_token_container_to_access_token(token_container: AccessTokenContainer) -> str:
        result = {
            'user_id': token_container.user_id,
            'role': token_container.role,
            'is_superuser': token_container.is_superuser,
            'verified': token_container.verified,
            'subscribed': token_container.subscribed,
            'created_at': token_container.created_at,
            'subscribed_till': token_container.subscribed_till,
            'active_till': (token_container.created_at +
                            get_jwt_settings().access_token_expire_minutes),
            'refresh_id': token_container.refresh_id,
            'refreshed_at': token_container.refreshed_at
        }

        return dict_to_jwt(result)

    @staticmethod
    def map_token_container_to_refresh_token(token_container: AccessTokenContainer) -> str:
        result = {
            'refresh_id': token_container.refresh_id,
            'user_id': token_container.user_id,
            'active_till': (token_container.created_at +
                            get_jwt_settings().refresh_token_expire_minutes),
        }
        return dict_to_jwt(result)

    @staticmethod
    def refresh_token_to_tuple(refresh_token: str) -> tuple[str, str, int] | None:
        result = dict_from_jwt(refresh_token)
        if not result:
            return None
        return result.get('refresh_id'), result.get('user_id'), result.get('active_till')
