from functools import wraps

from configs.settings import ElasticSettings
from db.models.search_requests.base_request import BaseRequest
from db.models.search_requests.films.search_all_films_request import \
    SearchAllFilmsRequest
from db.models.search_requests.films.search_film_request import \
    SearchFilmRequest
from db.models.search_requests.films.single_film_request import \
    SingleFilmRequest
from db.models.search_requests.genres.all_genres_request import \
    AllGenresRequest
from db.models.search_requests.genres.single_genre_request import \
    SingleGenreRequest
from db.models.search_requests.persons.all_persons_request import \
    AllPersonsRequest
from db.models.search_requests.persons.films_by_person_request import \
    FilmsByPersonRequest
from db.models.search_requests.persons.list_of_films_by_person_request import \
    ListOfFilmsByPersonRequest
from db.models.search_requests.persons.search_person_request import \
    SearchPersonRequest
from db.models.search_requests.persons.single_person_request import \
    SinglePersonRequest
from db.models.search_responses.base_response import BaseResponse
from db.search.search_storage import SearchStorage
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MultiMatch, Q


class ElasticStorage(SearchStorage):
    _settings = ElasticSettings()
    _elastic: AsyncElasticsearch | None = None

    @staticmethod
    def initialize(func):
        @wraps(func)
        async def inner(self, *args, **kwargs):
            if self._elastic is None:
                elastic_dsl = self._settings.model_dump()
                self._elastic = AsyncElasticsearch(**elastic_dsl)
            return await func(self, *args, **kwargs)

        return inner

    async def handle_request(self, request: BaseRequest) -> BaseResponse | None:
        result = None
        try:
            match request:
                case SingleFilmRequest() as single_film_request:
                    result = await self._create_single_film_request(
                        single_film_request
                    )
                case SearchFilmRequest() as search_film_request:
                    result = await self._create_search_film_request(
                        search_film_request
                    )
                case SearchAllFilmsRequest() as all_films_request:
                    result = await self._create_search_all_films_request(
                        all_films_request
                    )
                case SingleGenreRequest() as single_genre_request:
                    result = await self._create_single_genre_request(
                        single_genre_request
                    )
                case AllGenresRequest() as all_genres_request:
                    result = await self._create_all_genres_request(
                        all_genres_request
                    )
                case FilmsByPersonRequest() | ListOfFilmsByPersonRequest() \
                        as films_by_person_request:
                    result = await self._create_films_by_person_request(
                        films_by_person_request
                    )
                case SearchPersonRequest() as search_person_request:
                    result = await self._create_search_person_request(
                        search_person_request
                    )
                case AllPersonsRequest() as all_persons_request:
                    result = await self._create_all_persons_request(
                        all_persons_request
                    )
                case SinglePersonRequest() as single_person_request:
                    result = await self._create_single_person_request(
                        single_person_request.person_id
                    )
                case _:
                    raise ValueError('Unknown request type')
        except NotFoundError:
            return result
        result = self._converter.map(result, request)
        return result

    async def close(self):
        if self._elastic is not None:
            await self._elastic.close()

    @initialize
    async def _create_single_film_request(self, request: SingleFilmRequest) -> dict:
        return await self._elastic.get(index='movies', id=request.id)

    @initialize
    async def _create_single_genre_request(self, request: SingleGenreRequest) -> dict:
        return await self._elastic.get(index='genres', id=request.id)

    @initialize
    async def _create_search_film_request(self, request: SearchFilmRequest) -> dict:
        search_result = Search(using=self._elastic, index='movies').query(
            MultiMatch(query=request.query, fields=['title^5', 'description'])
        )

        return await self._paginate_films_request(search_result, request, request.sort)

    @initialize
    async def _create_search_all_films_request(self, request: SearchAllFilmsRequest) -> dict:
        search_result = Search(using=self._elastic, index='movies')
        if request.genres:
            genre_queries = [Q("nested",
                               path="genres",
                               query=Q("match",
                                       genres__id=genre_id)) for genre_id in request.genres]
            search_result = search_result.query(
                'bool', must=genre_queries
            )

        return await self._paginate_films_request(search_result, request, request.sort)

    @initialize
    async def _create_all_genres_request(self, request: AllGenresRequest) -> dict:
        search_result = Search(using=self._elastic, index='genres')
        return await self._paginate_genres_request(search_result, request)

    @initialize
    async def _create_films_by_person_request(self, request: FilmsByPersonRequest) -> dict:
        # todo надо проверять, что вообще возможно сделать запрос и что индекс существует

        search_result = Search(index='movies').query(
            Q('nested', path='actors',
              query=Q('term', **{'actors.id': request.person_id})) |
            Q('nested', path='directors',
              query=Q('term', **{'directors.id': request.person_id})) |
            Q('nested', path='writers',
              query=Q('term', **{'writers.id': request.person_id}))
        )
        return await self._elastic.search(index='movies', body=search_result.to_dict())

    @initialize
    async def _create_search_person_request(self, request: SearchPersonRequest) -> dict:
        search_result = Search(using=self._elastic, index='persons').query(
            Match(full_name={'query': request.query})
        )
        return await self._paginate_persons_request(search_result, request)

    @initialize
    async def _create_all_persons_request(self, request: AllPersonsRequest) -> dict:
        search_result = Search(using=self._elastic, index='persons')
        return await self._paginate_persons_request(search_result, request)

    @initialize
    async def _create_single_person_request(self, person_id: str) -> dict:
        return await self._elastic.get(index='persons', id=person_id)

    @initialize
    async def _paginate_films_request(
            self,
            search_result: Search,
            request: BaseRequest,
            sort: str = None
    ) -> dict:
        if sort:
            search_result = search_result.sort(request.sort)
        start = (request.page - 1) * request.size
        search_result = search_result[start:start + request.size]

        return await self._elastic.search(index='movies', body=search_result.to_dict())

    @initialize
    async def _paginate_genres_request(
            self,
            search_result: Search,
            request: BaseRequest
    ) -> dict:
        start = (request.page - 1) * request.size
        search_result = search_result[start:start + request.size]

        return await self._elastic.search(index='genres', body=search_result.to_dict())

    @initialize
    async def _paginate_persons_request(
            self,
            search_result: Search,
            request: BaseRequest
    ) -> dict:
        start = (request.page - 1) * request.size
        search_result = search_result[start:start + request.size]

        return await self._elastic.search(index='persons', body=search_result.to_dict())
