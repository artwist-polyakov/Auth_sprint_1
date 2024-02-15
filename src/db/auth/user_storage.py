from abc import ABC, abstractmethod

from db.auth.user_converter import UserConverter
from db.models.auth_requests.base_request import BaseRequest
from db.models.auth_responses.base_response import BaseResponse


class UserStorage(ABC):
    # регистрирует пользователя
    # содержит UsersDataSource, выбирает метод на основе request
    # возвращает Result

    def __init__(self, converter: UserConverter):
        self._converter = converter

    @abstractmethod
    def handle_request(self, request: BaseRequest) -> BaseResponse:
        pass
