import time
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EventType(str, Enum):
    PLAY = 'play'
    PAUSE = 'pause'
    STOP = 'stop'
    SEEK = 'seek'
    CHANGE_QUALITY = 'change_quality'
    MUTE = 'mute'
    UNMUTE = 'unmute'
    CHANGE_LANGUAGE = 'change_language'
    COMPLETE = 'complete'


class PlayerEvent(BaseModel):
    user_uuid: Optional[str] = None
    film_uuid: str
    event_type: EventType
    event_value: str | None = None
    timestamp: int = time.time_ns()
