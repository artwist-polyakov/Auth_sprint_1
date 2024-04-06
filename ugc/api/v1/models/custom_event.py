import time
from typing import Optional

from pydantic import BaseModel


class CustomEvent(BaseModel):
    user_uuid: str | None = None
    event_type: str
    timestamp: int = time.time_ns()
