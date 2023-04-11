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



if __name__ == '__main__00':
    frame0 = cv2.imread(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/0.png")
    frame1 = cv2.imread(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/1.png")
    frame2 = cv2.imread(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/2.png")
    frame3 = cv2.imread(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/3.png")
    frame4 = cv2.imread(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/4.png")
    frame5 = cv2.imread(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/5.png")
    # frame6 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/6.png")
    # frame7 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/7.png")
    # frame8 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/8.png")
    # frame9 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/9.png")
    # frame10 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/10.png")
    # frame11 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/log_saves/plate_change_orientation/11.png")

    # Init

    plate = get_chess_plate(frame0)
    game = Game(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #1

    plate = get_chess_plate(frame1)
    game.play_from_plate(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #2

    plate = get_chess_plate(frame2)
    game.play_from_move(chess.Move(
        chess.square(3, 6), chess.square(3, 4)), plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #3

    plate = get_chess_plate(frame3)
    game.play_from_plate(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #4

    plate = get_chess_plate(frame4)
    game.play_from_move(chess.Move(
        chess.square(2, 6), chess.square(2, 4)), plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #5

    plate = get_chess_plate(frame5)
    game.play_from_plate(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #6

    # plate = get_chess_plate(frame6)
    # game.play_from_move(chess.Move(
    #     chess.square(1, 6), chess.square(2, 4)), plate)
    # print(game.board)

    # plate.show()
    # cv2.waitKey(0)


# if __name__ == '__main__':
#     frame1 = cv2.imread(
#         "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/difference/1.png")

#     plate1 = get_chess_plate(frame1)
#     plate1.show()
#     cv2.waitKey(0)

# if __name__ == '__main__00':
#     url = "http://172.20.10.9:8080/video"
#     cap = VideoCapture(url)

#     frame1 = cap.read()

#     cv2.imshow("frame1", frame1)
#     cv2.waitKey(0)

#     plate1 = get_chess_plate(frame1)
#     plate1.show()
#     cv2.waitKey(0)

#     cv2.destroyAllWindows()


if __name__ == "__main__00":

    # url = "http://10.112.91.130:8080/video"
    # cap = VideoCapture(url)

    cap = VideoCaptureImageSimulation(
        "C:/Users/Romaric/DataScience/EchecsVision/echec_vision/images/Video test full image/", 'png')

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

