from enum import Enum

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationScenario(str, Enum):
    DAILY = "DAILY"  # лайки, комменты, подписки
    WEEKLY = "WEEKLY"  # статистика
    MONTHLY = "MONTHLY"  # отчеты
    WELCOME = "WELCOME"  # приветствие
    BIRTHDAY = "BIRTHDAY"  # поздравление с днем рождения
    MAILINGS = "MAILINGS"  # рассылки от админа
    NEWS = "NEWS"  # новые поступления каталога


class TasksParams(BaseModel):
    title: str = Field(
        ...,
        description="Notification title"
    )
    content: str = Field(
        ...,
        description="Notification message",

    )
    type: MessageType = Field(
        MessageType.EMAIL,
        description="Notification type"
    )

    scenario: NotificationScenario = Field(
        NotificationScenario.DAILY,
        description="Notification scenario"
    )
