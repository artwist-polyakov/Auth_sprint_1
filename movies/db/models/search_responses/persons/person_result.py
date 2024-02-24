from dataclasses import field

from db.models.search_responses.base_response import BaseResponse


class PersonResult(BaseResponse):
    id: str = field(default='')
    name: str = field(default='')
