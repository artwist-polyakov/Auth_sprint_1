import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Any, Optional

from loguru import logger


class BaseStorage(ABC):
    @abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = "storage.json"):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, "w") as outfile:
            json.dump(state, outfile)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, "r") as json_file:
                return json.load(json_file)
        except (FileNotFoundError, JSONDecodeError):
            logger.warning("No state file provided. Continue with default file")
            return dict()


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        try:
            state = self.storage.retrieve_state()
        except FileNotFoundError:
            state = dict()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        return self.storage.retrieve_state().get(key)
