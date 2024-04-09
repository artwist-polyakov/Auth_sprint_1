from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Server, Tag


API_PREFIX = "/ugc/v1"

info = Info(title="UGC Service API", version="1.0.0")
events = Tag(name="events", description="Event tracking system")
server = Server(url="http://localhost:5555", description="Local development server")

app = OpenAPI(__name__, info=info, doc_prefix="/ugc/openapi", servers=[server])
# app = Flask(__name__)

from api.v1.routes import event_blueprint  # noqa: F401, E402

app.register_api(event_blueprint)

CORS(app)

if __name__ == "__main__":
    app.run()
