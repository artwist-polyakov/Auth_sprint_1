from db.models.search_requests.base_request import BaseRequest


class SinglePersonRequest(BaseRequest):
    person_id: str
