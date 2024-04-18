import time
from http import HTTPStatus

from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from api.v1.routes.utils import InvalidTokenError, NoTokenError, _get_token_from_cookie
from app import API_PREFIX, events
from flask import Response, jsonify, request
from flask_openapi3 import APIBlueprint
from services.queue_service import get_queue_service

event_blueprint = APIBlueprint(
    "/events", __name__, url_prefix=API_PREFIX, abp_tags=[events], doc_ui=True
)


@event_blueprint.post("/view_event", summary="Record a view event")
def view_event(query: ViewEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    if not query.user_uuid:
        try:
            query.user_uuid = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return (
            jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}),
            HTTPStatus.OK,
        )
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post("/player_event", summary="Record a player event")
def player_event(query: PlayerEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    if not query.user_uuid:
        try:
            query.user_uuid = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return (
            jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}),
            HTTPStatus.OK,
        )
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post("/custom_event", summary="Record a custom event")
def custom_event(query: CustomEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    if not query.user_uuid:
        try:
            query.user_uuid = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
    status, result = get_queue_service().process_event(query)
    if status == HTTPStatus.OK:
        return (
            jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}),
            HTTPStatus.OK,
        )
    return jsonify({"status": "error", "details": result}), status
