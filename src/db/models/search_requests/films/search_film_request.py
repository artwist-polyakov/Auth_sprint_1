from db.models.search_requests.base_request import BaseRequest

PAGE_SIZE = 10


class SearchFilmRequest(BaseRequest):
    query: str
    page: int = 1
    size: int = PAGE_SIZE
    sort: str | None = None
