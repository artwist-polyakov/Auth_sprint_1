from db.models.search_requests.base_request import BaseRequest


class SingleFilmRequest(BaseRequest):
    id: str
