from abc import ABC, abstractmethod

from db.models.search_requests.base_request import BaseRequest
from db.models.search_responses.base_response import BaseResponse
from db.search.search_converter import SearchConverter


class SearchStorage(ABC):

    def __init__(self, converter: SearchConverter):
        self._converter = converter

    @abstractmethod
    def handle_request(self, request: BaseRequest) -> BaseResponse:
        pass

    @abstractmethod
    def close(self):
        pass
