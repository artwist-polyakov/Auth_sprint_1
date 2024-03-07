from db.auth.base import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Text,
                        UniqueConstraint)
from datetime import datetime


class YandexOAuth(Base):
    __tablename__ = 'yandex_oauth'
    __table_args__ = {'schema': 'users'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    default_email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    access_token = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    token_type = Column(String(50), nullable=False)
    expires_in = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.users.uuid'))
    user = relationship('User', back_populates='yandex_oauth')

    def __init__(self,
                 uuid: str,
                 default_email: str,
                 first_name: str,
                 last_name: str,
                 access_token: str,
                 refresh_token: str,
                 token_type: str,
                 expires_in: int) -> None:
        self.uuid = uuid
        self.default_email = default_email
        self.first_name = first_name
        self.last_name = last_name
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in
