from typing import Any

from db.models.auth_responses.base_response import BaseResponse


class BaseSuccess:
    # пользователь создан
    def answer(self):
        return True


class BaseFailure:
    def answer(self):
        return False


class BaseResult(BaseResponse):
    def __init__(self, answer_type, **data: Any):
        super().__init__(**data)
        self.answer_type: BaseSuccess | BaseFailure = answer_type

    def result(self):
        self.answer_type.answer()
