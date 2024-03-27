from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/view_event', methods=['POST'])
async def view_event():
    data = request.get_json()
    # user_uuid = data.get('user_uuid')
    # film_uuid = data.get('film_uuid')

    return jsonify({'message': f'View event recorded {data}'})


@app.route('/player_event', methods=['POST'])
async def player_event():
    data = request.get_json()
    # user_uuid = data.get('user_uuid')
    # film_uuid = data.get('film_uuid')
    # event_type = data.get('event_type')
    # timestamp = data.get('timestamp')

    return jsonify({'message': f'Player event recorded {data}'})


@app.route('/custom_event', methods=['POST'])
async def custom_event():
    data = request.get_json()

    return jsonify({'message': f'Custom event recorded {data}'})


if __name__ == '__main__':
    app.run()
