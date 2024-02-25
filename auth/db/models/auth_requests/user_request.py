from db.models.auth_requests.base_request import BaseRequest


class UserRequest(BaseRequest):
    uuid: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str = 'user'
    is_superuser: bool = False
    is_verified: bool = False
