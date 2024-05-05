from datetime import datetime
from db.base import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'users'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_superuser = Column(Boolean, default=0, nullable=False)
    role = Column(String(255), nullable=False, default='unauthorized')
    is_verified = Column(Boolean, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    refresh_tokens = relationship('RefreshToken', back_populates='user',
                                  cascade="all, delete-orphan")
    yandex_oauth = relationship('OAuth', back_populates='user',
                                cascade="all, delete-orphan")

    def __init__(self,
                 email: str,
                 password: str,
                 first_name: str,
                 last_name: str) -> None:
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f'<User {self.email}>'
