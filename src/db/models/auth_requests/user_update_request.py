from db.models.auth_requests.base_request import BaseRequest


class UserUpdateRequest(BaseRequest):
    uuid: str
    login: str
    first_name: str
    last_name: str
