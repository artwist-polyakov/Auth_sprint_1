from db.models.auth_requests.base_request import BaseRequest


class SignUpRequest(BaseRequest):
    login: str
    password: str
    first_name: str
    last_name: str
