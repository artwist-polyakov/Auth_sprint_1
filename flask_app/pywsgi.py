from gevent import monkey

from configs.settings import settings

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app import app


http_server = WSGIServer(('', settings.flask_port), app)
http_server.serve_forever()
