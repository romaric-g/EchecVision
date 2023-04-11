from core.server.types import GameLog
from flask_socketio import SocketIO, emit
from core.server.server import socketio 
import json

def push_game_log(self, game_log: GameLog):
    socketio.emit("new_game_log", json.dumps(game_log))

        
        