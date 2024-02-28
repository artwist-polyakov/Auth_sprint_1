
from typing import Generic, TypeVar

from api.v1.models.output import Output

T = TypeVar('T')


class PaginatedOutput(Output, Generic[T]):
    total: int
    page: int
    pages: int
    per_page: int
    results: list[T]
