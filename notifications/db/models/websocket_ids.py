from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String

from db.models.base import Base


class WebsocketConnections(Base):
    __tablename__ = 'websocket_connections'
    __table_args__ = (
        Index('ix_websocket_connections_user_id', 'user_id'),
        {'schema': 'notifications'},
    )

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: str = Column(String, nullable=False)
    websocket_id: str = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active: bool = Column(Boolean, nullable=False, default=True)
