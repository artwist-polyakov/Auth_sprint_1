from http import HTTPStatus
from flask import jsonify, Response
from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from app import app, events
from services.queue_service import get_queue_service
import time
API_PREFIX = '/ugc/v1'


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

@app.post(f'{API_PREFIX}/view_event', summary="Record a view event", tags=[events])
def view_event(query: ViewEvent) -> tuple[Response, int]:
    start_time = time.time()
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.time()-start_time} s"}), HTTPStatus.OK
    else:
        return jsonify({"status": "error", "details": result}), status


@app.post(f'{API_PREFIX}/player_event', summary="Record a player event", tags=[events])
def player_event(query: PlayerEvent) -> tuple[Response, int]:
    start_time = time.time()
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.time()-start_time} s"}), HTTPStatus.OK
    else:
        return jsonify({"status": "error", "details": result}), status


@app.post(f'{API_PREFIX}/custom_event', summary="Record a custom event", tags=[events])
def custom_event(query: CustomEvent) -> tuple[Response, int]:
    start_time = time.time()
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.time()-start_time} s"}), HTTPStatus.OK
    else:
        return jsonify({"status": "error", "details": result}), status
