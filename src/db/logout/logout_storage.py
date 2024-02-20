from abc import ABC, abstractmethod


class LogoutStorage(ABC):
    @abstractmethod
    def logout_current_session(self, access_token: str) -> None:
        pass

    @abstractmethod
    def logout_all_sessions(self, access_token: str) -> None:
        pass

    @abstractmethod
    def is_blacklisted(self, access_token: str) -> bool:
        pass
