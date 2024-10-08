from dataclasses import field

from db.models.auth_responses.base_response import BaseResponse


class UserResponse(BaseResponse):
    uuid: str
    email: str
    first_name: str = field(default='')
    last_name: str = field(default='')
