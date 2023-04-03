import time
import os
import numpy as np
import cv2 as cv2
import chess.engine
from core.camera.video_capture import VideoTimeSimultation
from core.movement.detector import MoveDetector
from core.utils.image_logger import ImageLogger


if __name__ == "__main__":

    # Create a VideoCapture object and read from input file
    cap = VideoTimeSimultation('Vidéo partie échec.mp4', 30)
    cap.start()

    played = input("Ready to start ?")

    log_path = 'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_demo_video'

    move_detector = MoveDetector(log_path)

    moovs = [
        chess.Move(chess.C7, chess.C5),
        chess.Move(chess.G8, chess.F6),
        chess.Move(chess.F6, chess.E4),
        chess.Move(chess.B8, chess.C6),
        chess.Move(chess.G7, chess.G5),
    ]

    # Read until video is completed
    while(cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
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
