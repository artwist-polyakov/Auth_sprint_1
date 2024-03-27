from api.v1.routes import register_routes
from flask import Flask

app = Flask(__name__)

# Регистрация ручек
register_routes(app)

if __name__ == '__main__':
    app.run()
