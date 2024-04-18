import time
from http import HTTPStatus
from uuid import UUID

import jwt
from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from app import API_PREFIX, events, films
from core.settings import settings
from flask import Response, jsonify, request
from flask_openapi3 import APIBlueprint
from services.queue_service import get_queue_service

from .models.bookmark import Bookmark
from .models.critique import Critique

event_blueprint = APIBlueprint(
    "/events", __name__, url_prefix=API_PREFIX, abp_tags=[events], doc_ui=True
)

films_blueprint = APIBlueprint(
    "/films", __name__, url_prefix=API_PREFIX, abp_tags=[films], doc_ui=True
)


class InvalidTokenError(Exception):
    pass


class NoTokenError(Exception):
    pass


def _get_token_from_cookie(request_container) -> str:
    access_token_cookie = request_container.cookies.get("access_token")
    if not access_token_cookie:
        raise NoTokenError("Access token not found")
    try:
        decoded_token = jwt.decode(
            access_token_cookie,
            settings.token.openssl_key,
            algorithms=[settings.token.algorithm],
        )
        return decoded_token["user_id"]
    except Exception:
        raise InvalidTokenError("Invalid token")


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


@films_blueprint.get(
    "/rated_films", summary="Get a list of films that the user has rated"
)
def get_rated_films(user_id: UUID) -> tuple[Response, int]:
    # 1/0 # for sentry test
    if not user_id:
        try:
            user_id = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка user_id
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@films_blueprint.get(
    "/film_rating_by_id", summary="Get a list of films that the user has rated"
)
def get_film_rating_by_id(film_id: UUID) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        user_id = _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@films_blueprint.post("/rating", summary="Add bookmark")
def add_rating(critique: Critique) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        user_id = _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@films_blueprint.delete("/rating", summary="Delete rating")
def delete_rating(critique_id: UUID) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        user_id = _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@films_blueprint.post("/bookmark", summary="Add bookmark")
def add_bookmark(critique: Bookmark) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        user_id = _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@films_blueprint.delete("/bookmark", summary="Delete bookmark")
def delete_bookmark(bookmark_id: UUID) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        user_id = _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400
