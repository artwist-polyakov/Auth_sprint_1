from flask import Blueprint, jsonify, request

routes = Blueprint('routes', __name__)


@routes.route('/view_event', methods=['POST'])
async def view_event():
    data = request.get_json()
    # user_uuid = data.get('user_uuid')
    # film_uuid = data.get('film_uuid')

    return jsonify({'message': f'View event recorded {data}'})


@routes.route('/player_event', methods=['POST'])
async def player_event():
    data = request.get_json()
    # user_uuid = data.get('user_uuid')
    # film_uuid = data.get('film_uuid')
    # event_type = data.get('event_type')
    # timestamp = data.get('timestamp')

    return jsonify({'message': f'Player event recorded {data}'})


@routes.route('/custom_event', methods=['POST'])
async def custom_event():
    data = request.get_json()

    return jsonify({'message': f'Custom event recorded {data}'})


def register_routes(app):
    app.register_blueprint(routes)
