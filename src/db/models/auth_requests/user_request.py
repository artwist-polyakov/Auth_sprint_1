import uuid

from db.models.auth_requests.base_request import BaseRequest


class UserRequest(BaseRequest):
    uuid: str = uuid.uuid4()
    login: str
    password: str
    first_name: str
    last_name: str
    is_verified: bool
