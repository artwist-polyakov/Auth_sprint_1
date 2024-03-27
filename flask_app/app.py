from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/view_event', methods=['POST'])
async def view_event():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    film_uuid = data.get('film_uuid')

    return jsonify({'message': 'View event recorded'})


@app.route('/player_event', methods=['POST'])
async def player_event():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    film_uuid = data.get('film_uuid')
    event_type = data.get('event_type')
    timestamp = data.get('timestamp')

    return jsonify({'message': 'Player event recorded'})


@app.route('/custom_event', methods=['POST'])
async def custom_event():
    data = request.get_json()

    return jsonify({'message': 'Custom event recorded'})


if __name__ == '__main__':
    app.run()
