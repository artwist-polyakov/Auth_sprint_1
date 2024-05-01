from enum import Enum

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


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
