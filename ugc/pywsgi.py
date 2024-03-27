from core.settings import settings
from gevent import monkey

monkey.patch_all()

from app import app  # noqa
from gevent.pywsgi import WSGIServer  # noqa

http_server = WSGIServer(('', settings.flask.port), app)
http_server.serve_forever()
