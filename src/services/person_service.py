from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.cache.cache_storage import CacheStorage
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
from db.models.search_responses.paginated_result import PaginatedResult
from db.models.search_responses.persons.films_brief_result import \
    ListFilmBriefResult
from db.models.search_responses.persons.person_work_result import \
    PersonWorkResult
from services.base_service import BaseService
from utils.creator_provider import get_creator
from utils.wrappers import cached

PAGE_SIZE = 10
creator = get_creator()


class PersonService(BaseService):

    async def _get_person_from_elastic(self, person_id: str) -> PersonWorkResult | None:
        request = SinglePersonRequest(person_id=person_id)
        result = await self._search.handle_request(request)
        if result:
            request = FilmsByPersonRequest(person_id=person_id)
            container = await self._search.handle_request(request)
            result.films = container.films
        return result

    @cached(result_type=PersonWorkResult)
    async def get_by_id(self, person_id: str) -> PersonWorkResult | None:
        return await self._get_person_from_elastic(person_id)

    @cached(result_type=PaginatedResult[PersonWorkResult])
    async def get_all_persons(
            self,
            page: int = 1,
            size: int = PAGE_SIZE
    ) -> PaginatedResult[PersonWorkResult]:
        request = AllPersonsRequest(page=page, size=size)
        result = await self._search.handle_request(request)
        return result

    @cached(result_type=ListFilmBriefResult)
    async def get_films_for_person_from_elastic(self, person_id: str) -> ListFilmBriefResult:
        request = ListOfFilmsByPersonRequest(person_id=person_id)
        result = await self._search.handle_request(request)
        return result if result else ListFilmBriefResult(results=[])

    @cached(result_type=PaginatedResult[PersonWorkResult])
    async def search_persons(
            self,
            query: str,
            page: int = 1,
            size: int = PAGE_SIZE
    ) -> PaginatedResult[PersonWorkResult]:
        request = SearchPersonRequest(query=query, page=page, size=size)
        result = await self._search.handle_request(request)
        if result:
            for person in result.results:
                request = FilmsByPersonRequest(person_id=person.id)

                # вернется объект класса ListFilmRoleResult
                list_object = await self._search.handle_request(request)
                person.films = list_object.films
        return result


@lru_cache()
def get_person_service(
        cache: CacheStorage = Depends(creator.get_cache_storage),
        search: AsyncElasticsearch = Depends(creator.get_search_storage),
) -> PersonService:
    return PersonService(cache, search)
