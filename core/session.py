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
from pathlib import Path
import json


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
    stockfish_path = r"C:\Users\Romaric\DataScience\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    url = "172.20.10.9:8080"
    url_connected = False
    url_error = False

    def __init__(self, load_config=False) -> None:

        self.load_config = load_config

        if load_config:
            file = open('settings.json')
            data = json.load(file)

            self.url = data["url"]
            self.stockfish_path = data["stockfish_path"]

    def start(self):

        print("START FCT")
        print(self.url)
        print(self.stockfish_path)

        if self.url == None:
            raise "Vous devez d'abord definir une url"

        if self.stockfish_path == None:
            raise "Vous devez d'abord définir le chemin d'acces à stockfish"

        try:
            with open(self.stockfish_path):
                pass
        except Exception:
            raise "Le chemin d'acces à stockfish n'existe pas !"

        if self.is_start:
            raise "La session a déjà commencé"

        self.is_start = True
        self.get_connector().update_game_state()
        self.get_connector().clear_game_log()

        socketio = self.get_socket()

        def start_thread(reader):
            socketio.start_background_task(reader)

        url = int(self.url) if is_int(
            self.url) else "http://" + str(self.url) + "/video"

        self.cap = VideoCapture(url, start_thread)

        socketio.start_background_task(self.start_loop)

    def start_loop(self, log_path='C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_demo_camera'):

        cap = self.cap

        engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

        self.move_detector = MoveDetector(log_path, engine)

        # La connection reseau semble affaiblire la qualité des premieres image renvoyé par l'appareil
        # On brule les premieres image reçu
        burn = 0
        burn_amount = 60

        try:

            # Read until video is completed
            while(self.is_start and burn < burn_amount):

                if self.is_pause:
                    continue

                # Capture frame-by-frame
                frame = cap.read(timeout=2)
                if frame is None:
                    time.sleep(1)
                    continue
                elif not self.url_connected:
                    self.url_connected = True
                    self.get_connector().update_url_data()

                burn = burn + 1

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
        self.stockfish_path = Path(settings["stockfish_path"])

        print("Set url", self.url)
        print("Set stockfish_path", self.stockfish_path)

        if self.load_config:
            out_file = open("settings.json", "w")

            json.dump({
                "url": str(self.url),
                "stockfish_path": str(self.stockfish_path)
            }, out_file, indent=6)

            out_file.close()

    def get_connector(self):
        from core.server.connector import connector
        return connector

    def get_socket(self):
        from core.server.server import socketio
        return socketio


session = Session(load_config=True)
