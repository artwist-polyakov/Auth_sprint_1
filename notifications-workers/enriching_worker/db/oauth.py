from datetime import datetime

from db.base import Base
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class OAuth(Base):
    __tablename__ = 'oauth'
    __table_args__ = {'schema': 'users'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    oauth_source = Column(String(50), nullable=False)
    token_type = Column(String(50), nullable=False)
    expires_in = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.users.uuid'))
    user = relationship('User', back_populates='yandex_oauth')

    def __init__(self,
                 uuid: str,
                 email: str,
                 first_name: str,
                 last_name: str,
                 access_token: str,
                 refresh_token: str,
                 oauth_source: str,
                 token_type: str,
                 expires_in: int) -> None:
        self.uuid = uuid
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.oauth_source = oauth_source
        self.token_type = token_type
        self.expires_in = expires_in
