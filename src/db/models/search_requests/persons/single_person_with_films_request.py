from db.models.search_requests.base_request import BaseRequest


class SinglePersonWithFilmsRequest(BaseRequest):
    person_id: str
