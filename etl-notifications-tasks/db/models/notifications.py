from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class Notifications(Base):
    __tablename__ = 'notifications'
    __table_args__ = {'schema': 'notifications'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('notifications.tasks.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sended: bool = Column(Boolean, nullable=False, default=False)
    is_error: bool = Column(Boolean, nullable=False, default=False)
    task = relationship("Tasks", back_populates="notifications")
