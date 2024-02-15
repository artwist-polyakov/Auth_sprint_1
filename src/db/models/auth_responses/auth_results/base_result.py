from typing import Any

from db.models.auth_responses.answer import Answer
from db.models.auth_responses.base_response import BaseResponse


class BaseResult(BaseResponse):
    def __init__(self, answer_type, **data: Any):
        super().__init__(**data)
        self.answer_type: Answer = answer_type

    def result(self):
        self.answer_type.get_message()
