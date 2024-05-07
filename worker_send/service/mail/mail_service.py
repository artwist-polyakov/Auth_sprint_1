from abc import ABC, abstractmethod


class MailService(ABC):
    @abstractmethod
    def send(
            self,
            email: str,
            subject: str,
            data: dict,
            template: str
    ) -> bool:
        pass
