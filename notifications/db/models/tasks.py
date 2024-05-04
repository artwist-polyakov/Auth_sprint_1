from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from db.models.base import Base


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationScenario(str, Enum):
    DAILY = "daily"  # лайки, комменты, подписки
    WEEKLY = "weekly"  # статистика
    MONTHLY = "monthly"  # отчеты
    WELCOME = "welcome"  # приветствие
    BIRTHDAY = "birthday"  # поздравление с днем рождения
    MAILINGS = "mailings"  # рассылки от админа
    NEWS = "news"  # новые поступления каталога


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'notifications'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(255), nullable=False)
    content: str = Column(String, nullable=False)
    user_ids: list[str] = Column(ARRAY(String), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    scenario = Column(
        SQLEnum(NotificationScenario),
        nullable=False,
        default=NotificationScenario.DAILY
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    is_launched: bool = Column(Boolean, nullable=False, default=False)
    notifications = relationship(
        "Notifications",
        back_populates="task",
        cascade="all, delete, delete-orphan"
    )
