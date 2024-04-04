import uuid
import random
from datetime import datetime
from enum import Enum

from db.models import Click, PlayerEvent, OtherEvent


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


class EventGenerator:
    def __init__(self, pg_instance):
        self._pg_instance = pg_instance
        self.films = None
        self.events_generators = [
            self.generate_click_event,
            self.generate_player_event,
            self.generate_other_event
        ]

    async def get_films(self):
        self.films = await self._pg_instance.get_films()

    def get_random_film_uuid(self):
        if not self.films:
            return None
        return random.choice(self.films)

    def generate_click_event(self):
        user_id = str(uuid.uuid4())
        movie_id = str(self.get_random_film_uuid())
        created = int(datetime.now().timestamp())
        return Click(user_id=user_id, movie_id=movie_id, created=created)

    def generate_player_event(self):
        user_id = str(uuid.uuid4())
        movie_id = str(self.get_random_film_uuid())
        type = random.choice(list(EventType))
        depth = random.randint(1, 10)
        created = int(datetime.now().timestamp())
        return PlayerEvent(user_id=user_id, movie_id=movie_id, type=type, depth=depth, created=created)

    def generate_other_event(self):
        user_id = str(uuid.uuid4())
        movie_id = str(self.get_random_film_uuid())
        type = random.choice(['custom_event_type1', 'custom_event_type2', 'custom_event_type3'])
        created = int(datetime.now().timestamp())
        return OtherEvent(user_id=user_id, movie_id=movie_id, type=type, created=created)
