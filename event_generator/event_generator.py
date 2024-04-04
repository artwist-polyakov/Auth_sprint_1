import asyncio
import uuid
import random
from datetime import datetime

from models.player_event import PlayerEvent, EventType
from models.view_event import ViewEvent
from models.custom_event import CustomEvent


class EventGenerator:
    def __init__(self):
        self.films = None
        self.events_generators = [
            self.generate_custom_event,
            self.generate_view_event,
            self.generate_player_event
        ]

    def get_random_film_uuid(self):
        if not self.films:
            return None
        return random.choice(self.films)

    def generate_custom_event(self):
        user_uuid = str(uuid.uuid4())
        event_type = random.choice(['custom_event_type1', 'custom_event_type2', 'custom_event_type3'])
        timestamp = int(datetime.now().timestamp())
        return CustomEvent(user_uuid=user_uuid, event_type=event_type, timestamp=timestamp)

    def generate_player_event(self):
        user_uuid = str(uuid.uuid4())
        film_uuid = str(self.get_random_film_uuid())
        event_type = random.choice(list(EventType))
        event_value = random.choice(['value1', 'value2', 'value3'])
        timestamp = int(datetime.now().timestamp())
        return PlayerEvent(user_uuid=user_uuid, film_uuid=film_uuid, event_type=event_type, event_value=event_value,
                           timestamp=timestamp)

    def generate_view_event(self):
        user_uuid = str(uuid.uuid4())
        film_uuid = str(uuid.uuid4())
        return ViewEvent(user_uuid=user_uuid, film_uuid=film_uuid)
