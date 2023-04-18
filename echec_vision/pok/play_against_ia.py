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

    url = "http://10.112.91.130:8080/video"
    cap = VideoCapture(url)

    # cap = VideoCaptureImageSimulation(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/Video test full image/", 'png')

    played = input("Ready to start ?")

    frame = cap.read()

    export_path = 'C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/logs_video_sequence'
    img_logger = ImageLogger(export_path)
    cropped_logger = ImageLogger(export_path, 'cropped')

    initial_plate = get_chess_plate(frame, True)

    img_logger.log(frame)
    cropped_logger.log(initial_plate.plate_img)

    initial_plate.show()
    cv2.waitKey(0)

    game = Game(initial_plate)
    engine = chess.engine.SimpleEngine.popen_uci(
        r"C:\Users\Romaric\DataScience\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

    board = game.board

    while not board.is_game_over():

        # Le joueur joue

        played = input("Press Enter to confirm your play...")

        frame = cap.read()
        plate = get_chess_plate(standard(frame), True)

        img_logger.log(frame)
        cropped_logger.log(plate.plate_img)

        plate.show()
        cv2.waitKey(0)

        game.play_from_plate(plate)
        print(game.board)

        # L'IA joue

        result = engine.play(board, chess.engine.Limit(time=0.1))

        print("L'IA a joué : ", result.move)
        played = input("Press Enter to confirm you report IA's play...")

        frame = cap.read()
        plate = get_chess_plate(standard(frame), True)

        img_logger.log(frame)
        cropped_logger.log(plate.plate_img)

        plate.show()
        cv2.waitKey(0)

        game.play_from_move(result.move, plate)
        print(game.board)

    engine.quit()
    cap.release()
    cv2.destroyAllWindows()

