from functools import lru_cache

from db.cache.cache_storage import CacheStorage
from db.models.search_requests.genres.all_genres_request import \
    AllGenresRequest
from db.models.search_requests.genres.single_genre_request import \
    SingleGenreRequest
from db.models.search_responses.genres.genre_result import GenreResult
from db.models.search_responses.paginated_result import PaginatedResult
from db.search.search_storage import SearchStorage
from fastapi import Depends
from services.base_service import BaseService
from utils.creator_provider import get_creator
from utils.wrappers import cached

PAGE_SIZE = 10
creator = get_creator()


class GenreService(BaseService):

    @cached(result_type=GenreResult)
    async def get_by_id(self, genre_id: str) -> GenreResult | None:
        request = SingleGenreRequest(id=genre_id)
        result = await self._search.handle_request(request)
        return GenreResult(**result.model_dump()) if result else None

    @cached(result_type=PaginatedResult[GenreResult])
    async def get_all_genres(
            self,
            page: int = 1,
            size: int = PAGE_SIZE
    ) -> PaginatedResult[GenreResult]:
        request = AllGenresRequest(page=page, size=size)
        return await self._search.handle_request(request)


@lru_cache()
def get_genre_service(cache: CacheStorage = Depends(creator.get_cache_storage),search: SearchStorage = Depends(creator.get_search_storage),
) -> GenreService:
    return GenreService(cache, search)
