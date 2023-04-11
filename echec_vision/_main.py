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
from core.server.connector import Connector
from core.server.types import GameLog
from core.server.server import socketio, app
from core.session import session
from multiprocessing import Process, Value
import json
import asyncio
import threading


def run(url, connector):

    cap = VideoCapture(url)
    log_path = 'C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_demo_camera'

    move_detector = MoveDetector(log_path)

    # Read until video is completed
    while(True):

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


def main():

    connector = Connector(socketio)

    for i in range(0, 100):

        gamelog = GameLog(
            user='player',
            message="La partie vient de commencer : " + str(i)
        )

        connector.push_game_log(gamelog)

        print(str(i))
        time.sleep(2)


# def background_thread():


#     time.sleep(1)
#     print("background_thread")

#     for i in range(0, 100):
#         print(str(i))
#         # socketio.emit("new_game_log", {"test": str(i)}, broadcast=True)


#         connector.push_game_log()
#         time.sleep(1)

if __name__ == '__main__':

    print("a", socketio)

    # recording_on = Value('b', True)
    # p = Process(target=main, args=(connector,))
    # p.start()
    # socketio.run(app, debug=False, port=5001)
    # p.join()

    # threading.Thread(target=lambda: socketio.run(
    #     app, use_reloader=False, port=5001)).start()

    # socketio.run(
    #     app, use_reloader=False, port=5001)

    print("BEFORE")
    # socketio.start_background_task(main)

    # threading.Thread(target=lambda: background_thread()).start()

    # threading.Thread(target=lambda: socketio.start_background_task(
    #     background_thread)).start()

    print("AFTER")
    socketio.run(app, debug=False, port=5001)

    # main(connector)

    # time.sleep(4)

    # for i in range(0, 100):
    #     print(str(i))
    #     socketio.emit("new_game_log", {"test": str(i)})
