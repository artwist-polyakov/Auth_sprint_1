import logging
import uuid

import sentry_sdk
from core.settings import SentrySettings, settings  # noqa: F401, E402
from flask import g, request
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Server, Tag

API_PREFIX = "/ugc/v1"

info = Info(title="UGC Service API", version="1.0.0")
events = Tag(name="Events", description="Event tracking system")
content = Tag(name="Content", description="Allows user to add, edit, and remove reviews to films")
bookmarks = Tag(name="Bookmarks", description="Alows user to add and remove bookmarks to films")
rates = Tag(name="Rates", description="Alows user to rate films or reviews")
server = Server(url="http://localhost:5555", description="Local development server")

sentry_sdk.init(
    dsn=SentrySettings().dsn,
    enable_tracing=SentrySettings().enable_tracing,
)

app = OpenAPI(__name__, info=info, doc_prefix="/ugc/openapi", servers=[server])


# app = Flask(__name__)


@app.before_request
def start_request():
    g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    logging.info(
        f"Request started. "
        f"Method: {request.method}, "
        f"URL: {request.url}, "
        f"X-Request-Id: {g.request_id}"
    )


@app.after_request
def end_request(response):
    response.headers["X-Request-Id"] = g.request_id
    logging.info(
        f"Request finished. "
        f"Method: {request.method}, "
        f"URL: {request.url}, "
        f"X-Request-Id: {g.request_id}"
    )
    return response


from api.v1.routes.events import event_blueprint  # noqa: F401, E402
from api.v1.routes.films import bookmarks_blueprint  # noqa: F401, E402
from api.v1.routes.films import content_blueprint  # noqa: F401, E402
from api.v1.routes.films import rates_blueprint  # noqa: F401, E402

app.register_api(event_blueprint)
app.register_api(content_blueprint)
app.register_api(bookmarks_blueprint)
app.register_api(rates_blueprint)

CORS(app)

if __name__ == "__main__":
    app.run()
