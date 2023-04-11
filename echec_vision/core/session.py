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
# from core.server.server import socketio, app, start_server
from core.server.types import GameLog
from multiprocessing import Process, Value
import json
import asyncio


class Session:

    is_start = False
    is_pause = False
    url = None

    def start(self, log_path='C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_demo_camera'):

        if self.url == None:
            raise "Vous devez d'abord definir une url"

        if self.is_start:
            raise "La session a déjà commencé"

        self.is_start = True

        cap = VideoCapture(self.url)
        move_detector = MoveDetector(log_path)

        # Read until video is completed
        while(self.is_start):

            if self.is_pause:
                continue

            # Capture frame-by-frame
            frame = cap.read()
            if frame is None:
                continue

            move_detector.next_frame(frame, debug=True)

            # Press Q on keyboard to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release
        # the video capture object
        cap.release()
        # Closes all the frames
        cv2.destroyAllWindows()

        print("Start")

    def pause(self):
        self.is_pause = True
        print("Pause")

    def resume(self):
        self.is_pause = False
        print("Resume")

    def stop(self):
        self.is_start = False
        print("Stop")

    def updateSettings(self, settings):
        self.url = settings["url"]

        print("Set url", self.url)


session = Session()
