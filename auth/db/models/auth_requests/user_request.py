from db.models.auth_requests.base_request import BaseRequest


class UserRequest(BaseRequest):
    uuid: str
    login: str
    password: str
    first_name: str
    last_name: str
    is_superuser: bool = False
    is_verified: bool = False
