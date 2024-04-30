from enum import Enum

from db.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum as SQLEnum

from sqlalchemy.orm import relationship


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'notifications'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(255), nullable=False)
    content: str = Column(String, nullable=False)
    user_ids: list[str] = Column(ARRAY(String), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    is_launched: bool = Column(Boolean, nullable=False, default=False)
    notifications = relationship(
        "Notifications",
        back_populates="task",
        cascade="all, delete, delete-orphan"
    )
