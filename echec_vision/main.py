import time
import os
import numpy as np
import cv2 as cv2
import chess.engine
from flask_socketio import SocketIO
from core.camera.video_capture import VideoTimeSimultation
from core.movement.detector import MoveDetector
from core.utils.image_logger import ImageLogger
from core.camera.video_capture import VideoCapture
from core.server.types import GameLog
from core.server.server import socketio, app
from core.session import session


if __name__ == '__main__':

    print("Program starting...")

    socketio.run(app, debug=False, port=5001)
