from db.models.auth_requests.base_request import BaseRequest


class SingleUserRequest(BaseRequest):
    id: str
