from db.models.auth_requests.base_request import BaseRequest


class UserRequest(BaseRequest):
    id: str
