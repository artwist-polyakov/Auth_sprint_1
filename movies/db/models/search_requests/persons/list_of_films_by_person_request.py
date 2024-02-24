from db.models.search_requests.base_request import BaseRequest


class ListOfFilmsByPersonRequest(BaseRequest):
    person_id: str
