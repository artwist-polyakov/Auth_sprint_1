import time
from http import HTTPStatus

import jwt
from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from app import API_PREFIX, events
from core.settings import settings
from flask import Response, jsonify, request
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


@event_blueprint.post("/view_event", summary="Record a view event")
def view_event(query: ViewEvent) -> tuple[Response, int]:
    start_time = time.monotonic()

    access_token_cookie = request.cookies.get('access_token')
    if not access_token_cookie:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED

    try:
        decoded_token = jwt.decode(
            access_token_cookie,
            settings.token.openssl_key,
            algorithms=[settings.token.algorithm]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), HTTPStatus.UNAUTHORIZED
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    user_id = decoded_token['user_id']
    event_instance = ViewEvent(
        user_uuid=user_id,
        film_uuid=query.film_uuid,
        timestamp=query.timestamp)
    status, result = get_queue_service().process_event(event_instance)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic()-start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post("/player_event", summary="Record a player event")
def player_event(query: PlayerEvent) -> tuple[Response, int]:
    start_time = time.monotonic()

    access_token_cookie = request.cookies.get('access_token')
    if not access_token_cookie:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED

    try:
        decoded_token = jwt.decode(
            access_token_cookie,
            settings.token.openssl_key,
            algorithms=[settings.token.algorithm]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), HTTPStatus.UNAUTHORIZED
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    user_id = decoded_token['user_id']
    event_instance = PlayerEvent(
        user_uuid=user_id,
        film_uuid=query.film_uuid,
        event_type=query.event_type,
        event_value=query.event_value,
        timestamp=query.timestamp)
    status, result = get_queue_service().process_event(event_instance)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic()-start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post("/custom_event", summary="Record a custom event")
def custom_event(query: CustomEvent) -> tuple[Response, int]:
    start_time = time.monotonic()

    access_token_cookie = request.cookies.get('access_token')
    if not access_token_cookie:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED

    try:
        decoded_token = jwt.decode(
            access_token_cookie,
            settings.token.openssl_key,
            algorithms=[settings.token.algorithm]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), HTTPStatus.UNAUTHORIZED
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    user_id = decoded_token['user_id']
    event_instance = CustomEvent(
        user_uuid=user_id,
        event_type=query.event_type,
        timestamp=query.timestamp)
    status, result = get_queue_service().process_event(event_instance)
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic()-start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status
