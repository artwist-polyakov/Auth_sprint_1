import logging
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

class InvalideTokenError(Exception):
    pass


class NoTokenError(Exception):
    pass


def _get_token_from_cookie(request_container) -> str:
    access_token_cookie = request_container.cookies.get('access_token')
    if not access_token_cookie:
        raise NoTokenError("Access token not found")
    try:
        decoded_token = jwt.decode(
            access_token_cookie,
            settings.token.openssl_key,
            algorithms=[settings.token.algorithm]
        )
        return decoded_token['user_id']
    except Exception as e:
        raise InvalideTokenError("Invalid token")


@event_blueprint.post("/view_event", summary="Record a view event")
def view_event(query: ViewEvent) -> tuple[Response, int]:
    start_time = time.monotonic()
    if not query.user_uuid:
        print("User uuid not found")
        try:
            query.user_uuid = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalideTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
    status, result = get_queue_service().process_event(query)
    print(f"Status: {status}, result: {result}")

    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post("/player_event", summary="Record a player event")
def player_event(query: PlayerEvent) -> tuple[Response, int]:
    start_time = time.monotonic()
    if not query.user_uuid:
        print("User uuid not found")
        try:
            query.user_uuid = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalideTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
    status, result = get_queue_service().process_event(query)
    print(f"Status: {status}, result: {result}")
    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status


@event_blueprint.post("/custom_event", summary="Record a custom event")
def custom_event(query: CustomEvent) -> tuple[Response, int]:
    start_time = time.monotonic()
    if not query.user_uuid:
        print("User uuid not found")
        try:
            query.user_uuid = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalideTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
    status, result = get_queue_service().process_event(query)
    print(f"Status: {status}, result: {result}")

    if status == HTTPStatus.OK:
        return jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}), HTTPStatus.OK
    return jsonify({"status": "error", "details": result}), status
