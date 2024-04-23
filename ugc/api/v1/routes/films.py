import time
from http import HTTPStatus

from api.v1.models.bookmark import Bookmark
from api.v1.models.bookmark_event import (DeleteBookmarkEvent,
                                          GetUserBookmarksEvent)
from api.v1.models.rate_event import (DeleteRateEvent, GetFilmRatingEvent,
                                      GetRatedFilmsEvent, GetRatedReviewsEvent,
                                      RateMovieSchema, RateReviewSchema)
from api.v1.models.review_event import (DeleteReviewEvent, GetUserReviewsEvent,
                                        ReviewEventSchema)
from api.v1.routes.utils import (InvalidTokenError, NoTokenError,
                                 _get_token_from_cookie)
from app import API_PREFIX, bookmarks, content, rates
from flask import Response, jsonify, request
from flask_openapi3 import APIBlueprint
from services.queue_service import get_queue_service

content_blueprint = APIBlueprint(
    "/content", __name__, url_prefix=API_PREFIX, abp_tags=[content], doc_ui=True
)

bookmarks_blueprint = APIBlueprint(
    "/bookmark", __name__, url_prefix=API_PREFIX, abp_tags=[bookmarks], doc_ui=True
)

rates_blueprint = APIBlueprint(
    "/rate", __name__, url_prefix=API_PREFIX, abp_tags=[rates], doc_ui=True
)


@rates_blueprint.get(
    "/rated_films", summary="Get a list of films that user has rated")
def get_rated_films(query: GetRatedFilmsEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    if not query:
        try:
            user_id = _get_token_from_cookie(request)
        except NoTokenError:
            return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка user_id
        return jsonify({"details": f"all good {user_id}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@rates_blueprint.get(
    "/rated_reviews", summary="Get a list of reviews that user has rated")
def get_rated_reviews(query: GetRatedReviewsEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        # Обработка user_id
        return jsonify({"details": f"all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@rates_blueprint.get("/film_rating", summary="Get movie rating by id")
def get_film_rating_by_id(query: GetFilmRatingEvent) -> tuple[Response, int]:
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


@rates_blueprint.post("/rate_film", summary="Add rating tp film")
def add_film_rating(query: RateMovieSchema) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@rates_blueprint.delete("/rate_film", summary="Delete rating from film")
def delete_film_rating(query: DeleteRateEvent) -> tuple[Response, int]:
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


@rates_blueprint.patch("/rate_film", summary="Edit rating to review")
def edit_film_rating(query: RateMovieSchema) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@rates_blueprint.post("/rate_review", summary="Add rating to review")
def add_review_rating(query: RateReviewSchema) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@rates_blueprint.delete("/rate_review", summary="Delete rating from review")
def delete_review_rating(query: DeleteReviewEvent) -> tuple[Response, int]:
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


@rates_blueprint.patch("/rate_review", summary="Edit rating to review")
def edit_review_rating(query: RateReviewSchema) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@content_blueprint.post("/review", summary="Add review")
def add_review(query: ReviewEventSchema) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@content_blueprint.patch("/review", summary="Edit review")
def edit_review(query: ReviewEventSchema) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@content_blueprint.get("/reviews", summary="Get reviews by user")
def get_reviews_by_user(query: GetUserReviewsEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка user_id
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@content_blueprint.delete("/review", summary="Delete review")
def delete_review(query: DeleteReviewEvent) -> tuple[Response, int]:
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


@bookmarks_blueprint.post("/bookmark", summary="Add bookmark")
def add_bookmark(query: Bookmark) -> tuple[Response, int]:
    # 1/0 # for sentry test
    start_time = time.monotonic()
    try:
        _get_token_from_cookie(request)
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


@bookmarks_blueprint.get("/bookmarks", summary="Get bookmarks by user")
def get_bookmarks_by_user(query: GetUserBookmarksEvent) -> tuple[Response, int]:
    # 1/0 # for sentry test
    try:
        _get_token_from_cookie(request)
    except NoTokenError:
        return jsonify({"error": "Access token not found"}), HTTPStatus.UNAUTHORIZED
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

    try:
        # Обработка user_id
        return jsonify({"details": "all good"}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400


@bookmarks_blueprint.delete("/bookmark", summary="Delete bookmark")
def delete_bookmark(query: DeleteBookmarkEvent) -> tuple[Response, int]:
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
