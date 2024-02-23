from typing import Generic, TypeVar

from db.models.search_responses.base_response import BaseResponse

T = TypeVar('T')


class PaginatedResult(BaseResponse, Generic[T]):

    total: int
    page: int
    pages: int
    per_page: int
    results: list[T]
