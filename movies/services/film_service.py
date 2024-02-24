from functools import lru_cache

from db.cache.cache_storage import CacheStorage
from db.models.search_requests.films.search_all_films_request import \
    SearchAllFilmsRequest
from db.models.search_requests.films.search_film_request import \
    SearchFilmRequest
from db.models.search_requests.films.single_film_request import \
    SingleFilmRequest
from db.models.search_responses.films.film_result import FilmResult
from db.models.search_responses.paginated_result import PaginatedResult
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from services.base_service import BaseService
from utils.creator_provider import get_creator
from utils.wrappers import cached

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
PAGE_SIZE = 10
creator = get_creator()


class FilmService(BaseService):

    @cached(result_type=FilmResult)
    async def get_by_id(self, film_id: str) -> FilmResult | None:
        request = SingleFilmRequest(id=film_id)
        result = await self._search.handle_request(request)
        return FilmResult(**result.model_dump()) if result else None

    @cached(result_type=PaginatedResult[FilmResult])
    async def search_films(
            self,
            query: str,
            page: int = 1,
            size: int = PAGE_SIZE,
            sort: str | None = None
    ) -> PaginatedResult[FilmResult]:
        request = SearchFilmRequest(query=query, page=page, size=size, sort=sort)
        return await self._search.handle_request(request)

    @cached(result_type=PaginatedResult[FilmResult])
    async def get_all_films(
            self,
            page: int = 1,
            size: int = PAGE_SIZE,
            sort: str | None = None,
            genres: list[str] = None
    ) -> PaginatedResult[FilmResult]:
        request = SearchAllFilmsRequest(page=page, size=size, sort=sort, genres=genres)
        return await self._search.handle_request(request)


@lru_cache()
def get_film_service(
        cache: CacheStorage = Depends(creator.get_cache_storage),
        search: AsyncElasticsearch = Depends(creator.get_search_storage)
) -> FilmService:
    return FilmService(cache, search)
