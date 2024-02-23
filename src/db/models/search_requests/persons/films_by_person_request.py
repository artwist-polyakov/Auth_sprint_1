from db.models.search_requests.base_request import BaseRequest


class FilmsByPersonRequest(BaseRequest):
    person_id: str
