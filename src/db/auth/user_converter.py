from abc import ABC, abstractmethod

from db.models.auth_requests.base_request import BaseRequest
from db.models.auth_responses.base_response import BaseResponse


class UserConverter(ABC):
    @abstractmethod
    def map(self, data: dict, request_type: BaseRequest) -> BaseResponse:
        pass
