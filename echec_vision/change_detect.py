import time
import os
import numpy as np
import cv2 as cv2
import chess.engine
from matplotlib import pyplot as plt
from get_chess_plate import *
from scipy import signal
from skimage.metrics import structural_similarity
from classes.game import *
from classes.video_capture import *
from classes.image_logger import *
from classes.chess_board_extractor import ChessBoardExtractor
from classes.sequence import Sequence
from functions.images.difference import *


if __name__ == "__main__":
    url = "Vidéo partie échec.mp4"
    cap = cv2.VideoCapture(url)

    last_extractor: ChessBoardExtractor = None

    # MOOV | STOP | FIX
    state = "FIX"

    moov_sequence = Sequence(10, 1)
    stop_sequence = Sequence(3)
    fix_sequence = Sequence(5, 1)

    def get_sequence(state):
        if state == "MOOV":
            return moov_sequence
        if state == "STOP":
            return stop_sequence
        if state == "FIX":
            return fix_sequence
        return None

    while(cap.isOpened()):
        _, frame = cap.read()

        if frame is None:
            continue

        extractor = ChessBoardExtractor(frame)
      
        if last_extractor != None:
            h = last_extractor.h, 

            print(h)

            a = cv2.warpPerspective(last_extractor.standard_image, *h, (700, 700))
            b = cv2.warpPerspective(extractor.standard_image, *h, (size, size))

            show_difference(a, b)

            # b_new = imutils.resize(b, height=600)

            # score = compute_difference_score(a, b, 10000)
        
            # color = (0, 255, 0) if score > 250 else (0, 0, 255)
            # image = cv2.putText(b_new, str(score), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
            #        1, color, 2, cv2.LINE_AA)

            # cv2.imshow("image", image)
            # cv2.waitKey(1)


        plate = extractor.extract()   

        if plate.is_valide():
            last_extractor = extractor


        