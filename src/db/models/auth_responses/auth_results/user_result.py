from dataclasses import field

from db.models.auth_responses.base_response import BaseResponse


class UserResult(BaseResponse):
    id: str = field(default='')
    login: str = field(default='')
    password: str = field(default='')
    first_name: str = field(default='')
    last_name: str = field(default='')
