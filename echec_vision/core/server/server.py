#import eventlet
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import threading
from flask_cors import CORS
from core.server.connector import connector
from core.session import session
import time

app = Flask(__name__, static_folder="dist/assets", template_folder="dist")
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
#socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
# eventlet.monkey_patch()


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data': 'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)


@app.route("/init")
def init_call():
    print("INIT", str(connector.get_session().stockfish_path))
    data = {
        'game_logs': connector.game_logs_dumps,
        'chess_board_state': connector.chess_board_state_dumps,
        'stockfish_path': str(connector.get_session().stockfish_path),
        'url': connector.get_session().url,
        'url_connected': connector.get_session().url_connected,
        'url_error': connector.get_session().url_error,
        'is_pause': connector.get_session().is_pause,
        'is_start': connector.get_session().is_start,

    }
    return jsonify(data)


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on('start')
def handle_start():
    """event listener when client start game"""
    try:
        print("ACTION : START")
        session.start()

    except Exception as e:
        print("Error on starting game", e)


@socketio.on('pause')
def handle_pause(data):
    """event listener when client pause game"""
    try:
        print("ACTION : PAUSE")
        session.pause()
    except:
        print("Error on pausing game")


@socketio.on('resume')
def handle_resume(data):
    """event listener when client resume game"""
    try:
        print("ACTION : RESUME")
        session.resume()
    except:
        print("Error on resuming game")


@socketio.on('stop')
def handle_resume():
    """event listener when client stop game"""
    try:
        print("ACTION : STOP")
        session.stop()
    except:
        print("Error on stoping game")


@socketio.on('settings')
def handle_resume(data):
    """event listener when client save game settings"""

    print("on settings")

    session.updateSettings(data)


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


# @app.before_first_request
# def your_function():
#     print("execute before server starts")

#     connector = Connector(socketio)

#     for i in range(0, 100):

#         gamelog = GameLog(
#             user='player',
#             message="La partie vient de commencer : " + str(i)
#         )

#         connector.push_game_log(gamelog)

#         print(str(i))


def start_server():
    global socketio, app

    socketio.run(app, debug=False, port=5001)


if __name__ == '__main__':
    start_server()
