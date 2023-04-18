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


def is_int(element: any) -> bool:
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        int(element)
        return True
    except ValueError:
        return False


class Session:

    is_start = False
    is_pause = False
    url = "192.168.1.34:8080"
    url_connected = False
    url_error = False

    def start(self):

        print("START FCT")
        print(self.url)

        if self.url == None:
            raise "Vous devez d'abord definir une url"

        if self.is_start:
            raise "La session a déjà commencé"

        self.is_start = True
        self.get_connector().update_game_state()

        socketio = self.get_socket()

        def start_thread(reader):
            socketio.start_background_task(reader)

        url = int(self.url) if is_int(
            self.url) else "http://" + str(self.url) + "/video"

        self.cap = VideoCapture(url, start_thread)

        socketio.start_background_task(self.start_loop)

    def start_loop(self, log_path='C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_demo_camera'):

        cap = self.cap
        self.move_detector = MoveDetector(log_path)

        try:

            # Read until video is completed
            while(self.is_start):

                if self.is_pause:
                    continue

                # Capture frame-by-frame
                frame = cap.read(timeout=2)
                if frame is None:
                    continue
                elif not self.url_connected:
                    self.url_connected = True
                    self.get_connector().update_url_data()

                self.move_detector.next_frame(frame, debug=True)
                # Press Q on keyboard to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release
            # the video capture object
            cap.release()
            # Closes all the frames
            cv2.destroyAllWindows()
        except Exception as e:

            print("START ERROR : ", e)

            self.is_start = False
            self.is_pause = False
            self.url_error = True
            self.get_connector().update_url_data()

        print("end Start")

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

    def get_connector(self):
        from core.server.connector import connector
        return connector

    def get_socket(self):
        from core.server.server import socketio
        return socketio


session = Session()
