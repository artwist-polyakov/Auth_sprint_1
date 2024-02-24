from enum import Enum
from http import HTTPStatus

from api.v1.models.films.detailed_film import DetailedFilm
from api.v1.models.films.film import Film
from api.v1.models.paginated_output import PaginatedOutput
from api.v1.models.paginated_params import PaginatedParams
from api.v1.utils.api_convertor import APIConvertor
from fastapi import APIRouter, Depends, HTTPException, Query
from services.film_service import FilmService, get_film_service

router = APIRouter()
convertor = APIConvertor()


class SortOrder(str, Enum):
    ASC_IMDB = "imdb_rating"
    DESC_IMDB = "-imdb_rating"


@router.get(
   path='/search',
   response_model=PaginatedOutput[Film],
   summary="Search Films",
   description="Get a list of films based on a search query"
)
async def search_films(
        query: str = Query(..., alias="query"),
        pagination: PaginatedParams = Depends(),
        film_service: FilmService = Depends(get_film_service)
) -> PaginatedOutput[Film]:
    search_results = await film_service.search_films(
        query=query,
        page=pagination.page,
        size=pagination.size
    )
    # не знаю как сделать, чтобы тип возвращаемого значения считался за PaginatedOutput[Film]
    return convertor.map_films(search_results)


@router.get(
   path='/',
   response_model=PaginatedOutput[Film],
   summary="Get All Films",
   description="Get a list of all films with the ability "
               "to sort by IMDB rating and filter by one or several genres"
)
async def get_films(
        pagination: PaginatedParams = Depends(),
        sort: SortOrder = Query(None, alias="sort"),
        genres: list[str] = Query([], alias="genres"),
        film_service: FilmService = Depends(get_film_service)
) -> PaginatedOutput[Film]:
    search_results = await film_service.get_all_films(
        page=pagination.page,
        size=pagination.size,
        sort=sort,
        genres=genres
    )
    return convertor.map_films(search_results)


@router.get(
   path='/{film_id}',
   response_model=DetailedFilm,
   summary="Film Details",
   description="Get detailed information about a film based on its identifier"
)
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> DetailedFilm:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return convertor.map_films(film)
