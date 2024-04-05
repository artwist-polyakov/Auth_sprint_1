import time
from http import HTTPStatus

from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from app import API_PREFIX, events
from flask import Response, jsonify
from flask_openapi3 import APIBlueprint
from services.queue_service import get_queue_service

event_blueprint = APIBlueprint(
    "/events", __name__, url_prefix=API_PREFIX, abp_tags=[events], doc_ui=True
)

# """
# curl -X POST http://localhost:5555/ugc/v1/view_event \
#  -H "Content-Type: application/json" \
#  -d '{
#        "user_uuid": "user1",
#        "film_uuid": "film1"
#      }'
# {"status":"ok"}
#     :param query:
#     :return:
#     """


@event_blueprint.post(f"/view_event", summary="Record a view event")
def view_event(query: ViewEvent) -> tuple[Response, int]:
    start_time = time.monotonic()
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic()-start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post(f"/player_event", summary="Record a player event")
def player_event(query: PlayerEvent) -> tuple[Response, int]:
    start_time = time.monotonic()
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic()-start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post(f"/custom_event", summary="Record a custom event")
def custom_event(query: CustomEvent) -> tuple[Response, int]:
    start_time = time.monotonic()
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic()-start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status
