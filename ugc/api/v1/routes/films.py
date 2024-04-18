import time
from http import HTTPStatus
from uuid import UUID

from api.v1.models.bookmark import Bookmark
from api.v1.models.critique import Critique
from api.v1.routes.utils import InvalidTokenError, NoTokenError, _get_token_from_cookie
from app import API_PREFIX, films
from flask import Response, jsonify, request
from flask_openapi3 import APIBlueprint
from services.queue_service import get_queue_service

films_blueprint = APIBlueprint(
    "/films", __name__, url_prefix=API_PREFIX, abp_tags=[films], doc_ui=True
)


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


@films_blueprint.get("/film_rating_by_id", summary="Get movie by id")
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
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    status, result = get_queue_service().process_event(critique)
    if status == HTTPStatus.OK:
        return (
            jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}),
            HTTPStatus.OK,
        )
    return jsonify({"status": "error", "details": result}), status


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
def add_bookmark(bookmark: Bookmark) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    status, result = get_queue_service().process_event(bookmark)
    if status == HTTPStatus.OK:
        return (
            jsonify({"status": f"ok, speed = {time.monotonic() - start_time} s"}),
            HTTPStatus.OK,
        )
    return jsonify({"status": "error", "details": result}), status


@films_blueprint.delete("/bookmark", summary="Delete bookmark")
def delete_bookmark(bookmark_id: UUID) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400
