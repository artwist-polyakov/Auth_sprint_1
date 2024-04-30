from db.models.base import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Notifications(Base):
    __tablename__ = 'notifications'
    __table_args__ = {'schema': 'notifications'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('notifications.tasks.id'), nullable=False)
    is_sended: bool = Column(Boolean, nullable=False, default=False)
    task = relationship("Tasks", back_populates="notifications")
