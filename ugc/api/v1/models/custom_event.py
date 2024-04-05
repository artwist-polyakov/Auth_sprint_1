import time

from pydantic import BaseModel
from typing import Optional


class CustomEvent(BaseModel):
    user_uuid: Optional[str] = None
    event_type: str
    timestamp: int = time.time_ns()
