from db.models.search_requests.base_request import BaseRequest

PAGE_SIZE = 10


class AllPersonsRequest(BaseRequest):
    page: int = 1,
    size: int = PAGE_SIZE
