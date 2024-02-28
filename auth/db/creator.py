from abc import ABC, abstractmethod

from db.logout.logout_storage import LogoutStorage


class Creator(ABC):
    @abstractmethod
    def get_logout_storage(self) -> LogoutStorage:
        pass
