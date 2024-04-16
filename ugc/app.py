import uuid

from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Server, Tag
from flask import g, request
import logging
from core.settings import settings  # noqa: F401, E402

API_PREFIX = "/ugc/v1"

info = Info(title="UGC Service API", version="1.0.0")
events = Tag(name="events", description="Event tracking system")
server = Server(url="http://localhost:5555", description="Local development server")

app = OpenAPI(__name__, info=info, doc_prefix="/ugc/openapi", servers=[server])


# app = Flask(__name__)

@app.before_request
def start_request():
    g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    logging.info(f"Request started. "
                 f"Method: {request.method}, "
                 f"URL: {request.url}, "
                 f"X-Request-Id: {g.request_id}")


@app.after_request
def end_request(response):
    response.headers["X-Request-Id"] = g.request_id
    logging.info(f"Request finished. "
                 f"Method: {request.method}, "
                 f"URL: {request.url}, "
                 f"X-Request-Id: {g.request_id}")
    return response


from api.v1.routes import event_blueprint  # noqa: F401, E402

app.register_api(event_blueprint)

CORS(app)

if __name__ == "__main__":
    app.run()
