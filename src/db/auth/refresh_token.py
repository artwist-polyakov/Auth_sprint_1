from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from configs.settings import settings
from db.auth.user import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.users.uuid'), nullable=False)
    active_till = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='refresh_tokens')

    def __init__(self,
                 uuid: str,
                 user_id: str,
                 active_till: int) -> None:
        self.uuid = uuid
        self.user_id = user_id
        self.active_till = active_till
