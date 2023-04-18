import time
import os
import numpy as np
import cv2 as cv2
import chess.engine
from core.camera.video_capture import VideoTimeSimultation
from core.movement.detector import MoveDetector
from core.utils.image_logger import ImageLogger
from core.camera.video_capture import VideoCapture

if __name__ == "__main__":

    # Create a VideoCapture object and read from input file
    # Create a VideoCapture object and read from input file
    # url = "http://10.112.91.130:8080/video"
    url = "http://172.20.10.11:8080/video"
    cap = VideoCapture(url)

    played = input("Ready to start ?")

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
