from db.models.search_requests.base_request import BaseRequest

PAGE_SIZE = 10


class SearchAllFilmsRequest(BaseRequest):
    page: int = 1,
    size: int = PAGE_SIZE,
    sort: str | None = None,
    genres: list[str] = None
