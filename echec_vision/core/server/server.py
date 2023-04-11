import eventlet
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from core.server.types import GameLog
from core.session import session
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
eventlet.monkey_patch()


@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data': 'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    emit("data", {'data': data, 'id': request.sid}, broadcast=True)


@socketio.on('start')
def handle_start(data):
    """event listener when client start game"""
    try:
        socketio.start_background_task(session.start)
    except:
        print("Error on starting game")


@socketio.on('pause')
def handle_pause(data):
    """event listener when client pause game"""
    try:
        session.pause()
    except:
        print("Error on pausing game")


@socketio.on('resume')
def handle_resume(data):
    """event listener when client resume game"""
    try:
        session.resume()
    except:
        print("Error on resuming game")


@socketio.on('stop')
def handle_resume(data):
    """event listener when client stop game"""
    try:
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
