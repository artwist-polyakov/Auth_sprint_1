from abc import ABC, abstractmethod

from db.models.search_requests.base_request import BaseRequest
from db.models.search_responses.base_response import BaseResponse


class SearchConverter(ABC):
    @abstractmethod
    def map(self, data: dict, request_type: BaseRequest) -> BaseResponse:
        pass
