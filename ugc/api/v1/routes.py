from typing import List

from app import app, events
from pydantic import BaseModel, Field

API_PREFIX = '/ugc/v1'


# Модели Pydantic
class ViewEvent(BaseModel):
    user_uuid: str
    film_uuid: str


class PlayerEvent(BaseModel):
    user_uuid: str
    film_uuid: str
    event_type: str
    timestamp: int


class CustomEvent(BaseModel):
    user_uuid: str
    event_type: str
    timestamp: int


# curl -X POST http://localhost:5555/ugc/v1/view_event \
#  -H "Content-Type: application/json" \
#  -d '{
#    "events": [
#      {
#        "user_uuid": "user1",
#        "film_uuid": "film1"
#      },
#      {
#        "user_uuid": "user2",
#        "film_uuid": "film2"
#      }
#    ]
#  }'
# {"status":"ok"}
#     :param query:
#     :return:
#     """

class ListOfViewEvents(BaseModel):
    events: List[ViewEvent] = Field(..., description="List of view events")


@app.post(f'{API_PREFIX}/view_event', summary="Record a view event", tags=[events])
def view_event(query: ViewEvent):
    return {"status": "ok"}


@app.post(f'{API_PREFIX}/player_event', summary="Record a player event", tags=[events])
def player_event(query: PlayerEvent):
    return {"status": "ok"}


@app.post(f'{API_PREFIX}/custom_event', summary="Record a custom event", tags=[events])
def custom_event(query: CustomEvent):
    return {"status": "ok"}
