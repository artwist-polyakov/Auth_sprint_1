from datetime import datetime

# from configs.settings import settings
from db.auth.base import Base
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Text,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = (UniqueConstraint('uuid', 'user_device_type'),
                      {'schema': 'users',
                       'postgresql_partition_by': 'LIST (user_device_type)'})

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.users.uuid'), nullable=False)
    active_till = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_device_type = Column(Text, nullable=False, primary_key=True)
    user = relationship('User', back_populates='refresh_tokens')

    def __init__(self,
                 uuid: str,
                 user_id: str,
                 active_till: int,
                 user_device_type: str) -> None:
        self.uuid = uuid
        self.user_id = user_id
        self.active_till = active_till
        self.user_device_type = user_device_type
