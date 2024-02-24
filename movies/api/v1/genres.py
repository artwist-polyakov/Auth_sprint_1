from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models.genres.detailed_genre import DetailedGenre
from api.v1.models.genres.genre import Genre
from api.v1.models.paginated_output import PaginatedOutput
from api.v1.models.paginated_params import PaginatedParams
from api.v1.utils.api_convertor import APIConvertor
from services.genre_service import GenreService, get_genre_service

router = APIRouter()
convertor = APIConvertor()


@router.get(
    path='/{genre_id}',
    response_model=DetailedGenre,
    summary="Genre Details",
    description="Get detailed information about a genre based on its identifier"
)
async def genre_details(
        genre_id: str,
        genre_service=Depends(get_genre_service)
) -> DetailedGenre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return convertor.map_genres(genre)


@router.get(
    path='/',
    response_model=PaginatedOutput[Genre],
    summary="Get All Genres",
    description="Get a list of all genres"
)
async def get_genres(
        pagination: PaginatedParams = Depends(),
        genre_service: GenreService = Depends(get_genre_service)
) -> PaginatedOutput[Genre]:
    search_results = await genre_service.get_all_genres(
        page=pagination.page,
        size=pagination.size
    )
    return convertor.map_genres(search_results)
