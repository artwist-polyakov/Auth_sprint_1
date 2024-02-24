from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.models.paginated_output import PaginatedOutput
from api.v1.models.paginated_params import PaginatedParams
from api.v1.models.persons.film_brief import FilmBrief
from api.v1.models.persons.person import Person
from api.v1.models.persons.person_films import PersonFilms
from api.v1.utils.api_convertor import APIConvertor
from services.person_service import PersonService, get_person_service

router = APIRouter()
convertor = APIConvertor()


@router.get(
    path='/search',
    response_model=PaginatedOutput[PersonFilms],
    summary="Search Persons",
    description="Get a list of persons based on a search query"
)
async def search_persons(
        query: str = Query(..., alias="query"),
        pagination: PaginatedParams = Depends(),
        person_service: PersonService = Depends(get_person_service)
) -> PaginatedOutput[PersonFilms]:
    search_results = await person_service.search_persons(
        query=query,
        page=pagination.page,
        size=pagination.size
    )
    return convertor.map_persons(search_results)


@router.get(
    path='/{person_id}/film',
    response_model=list[FilmBrief],
    summary="Person's Films",
    description="Get a list of films for a person based on their identifier"
)
async def get_films(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> list[FilmBrief]:
    search_results = await (
        person_service.get_films_for_person_from_elastic(person_id))
    return convertor.map_persons(search_results)


@router.get(
    path='/{person_id}',
    response_model=PersonFilms,
    summary="Person Details",
    description="Get detailed information about a person based on their identifier"
)
async def person_details(
        person_id: str,
        person_service=Depends(get_person_service)
) -> PersonFilms:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return convertor.map_persons(person)


@router.get(
    path='/',
    response_model=PaginatedOutput[Person],
    summary="Get All Persons",
    description="Get a list of all persons"
)
async def get_persons(
        pagination: PaginatedParams = Depends(),
        person_service: PersonService = Depends(get_person_service)
) -> PaginatedOutput[Person]:
    search_results = await person_service.get_all_persons(
        page=pagination.page,
        size=pagination.size
    )
    # тут нельзя без brief — потому что сервис не возвращает фильмы актёров
    return convertor.map_persons(search_results, 'brief')
