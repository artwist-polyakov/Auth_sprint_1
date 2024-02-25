from datetime import datetime

from configs.settings import settings
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_superuser = Column(Boolean, default=0, nullable=False)
    role = Column(String(255), nullable=False, default='unauthorized')
    is_verified = Column(Boolean, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    refresh_tokens = relationship('RefreshToken', back_populates='user',
                                  cascade="all, delete-orphan")

    def __init__(self,
                 login: str,
                 password: str,
                 first_name: str,
                 last_name: str) -> None:
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f'<User {self.login}>'