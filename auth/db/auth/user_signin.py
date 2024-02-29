import datetime

import uuid
# from configs.settings import settings
from sqlalchemy import UniqueConstraint, Column, ForeignKey, DateTime, Text, text, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from db.auth.base import Base


DEVICES: list = ['mac_app', 'android_app', 'web', 'smart_tv']
# app может быть на телефоне и на планшете


def create_partition(target, connection, **kw) -> None:
    """creating partition by user_sign_in"""

    for device in DEVICES:
        connection.execute(
            text(
                f"CREATE TABLE IF NOT EXISTS 'users_sign_in_{device}' "
                f"PARTITION OF 'users_sign_in' FOR VALUES IN ('{device}')"
            )
        )


class UserSignIn(Base):
    __tablename__ = 'users_sign_in'
    __table_args__ = (
        UniqueConstraint('uuid', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        }
    )

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.users.uuid'),
        nullable=False
    )
    logged_in_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_agent = Column(Text)
    user_device_type = Column(Text, primary_key=True)

    def __init__(self,
                 user_id: str,
                 logged_in_at: str,
                 user_agent: str,
                 user_device_type: str) -> None:
        self.user_id = user_id
        self.logged_in_at = logged_in_at
        self.user_agent = user_agent
        self.user_device_type = user_device_type

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logged_in_at}>'
