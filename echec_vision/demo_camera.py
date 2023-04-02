import time
import os
import numpy as np
import cv2 as cv2
import chess.engine
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity
from classes.game import *
from classes.video_capture import *
from classes.image_logger import *
from classes.chess_board_extractor import ChessBoardExtractor
from classes.sequence import Sequence
from functions.images.difference import *

if __name__ == "__main__":

    # Create a VideoCapture object and read from input file
    url = "http://10.112.91.130:8080/video"
    cap = VideoCapture(url)

    # GLOBAL
    extractors = list()
    last_time = time.time()

    # CONFIG
    relative_depth = 5
    size = 700
    threshold = 1000

    LM__MIN_RELATIVE_MOOV = 1.5

    NS__MIN_ABSOLUTE_MOOV = 2.5
    NS__MIN_RELATIVE_FIX = 1.5
    NS__MAX_UNVALIDE_PLATE = .5

    # STATE
    state_extractor = None
    last_valid_extractor = None
    long_moov_detected = False

    # COUNT
    relative_moov_time = 0
    relative_fix_time = 0
    absolute_moov_time = 0
    unvalide_plate_time = 0

    def push_extractor(extractor):
        if len(extractors) >= relative_depth:
            extractors.pop(0)
        extractors.append(extractor)

    def new_state(extractor):
        global long_moov_detected, state_extractor, relative_moov_time, relative_fix_time, absolute_moov_time, unvalide_plate_time
        state_extractor = extractor
        long_moov_detected = False

        relative_moov_time = 0
        relative_fix_time = 0
        absolute_moov_time = 0
        unvalide_plate_time = 0

    played = input("Ready to start ?")

    last_time = time.time()
    frame = cap.read()

    export_path = 'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_demo_camera'
    img_logger = ImageLogger(export_path)
    cropped_logger = ImageLogger(export_path, 'cropped')

    game = None
    engine = chess.engine.SimpleEngine.popen_uci(
        r"C:\Users\Romaric\DataScience\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

    # Read until video is completed
    while(True):

        now = time.time()
        diff_time = now - last_time
        last_time = now

        # Capture frame-by-frame
        frame = cap.read()

        # Periode de setup
        if game == None:
            extractor = ChessBoardExtractor(frame)
            push_extractor(extractor)

            extract = extractor.extract()

            cv2.imshow("changes", frame)

            if extract.is_valide():
                initial_plate = extractor.chess_plate
                game = Game(initial_plate)
                state_extractor = extractor
                last_valid_extractor = extractor

                img_logger.log(frame)
                cropped_logger.log(initial_plate.plate_img)

            continue

        # Si la mise en place a déjà été faite

        current_extractor = ChessBoardExtractor(frame)
        push_extractor(current_extractor)

        relative_extractor: ChessBoardExtractor = extractors[0]
        absolute_extractor = state_extractor

        h = last_valid_extractor.h

        current_image = cv2.warpPerspective(
            current_extractor.standard_image, h, (700, 700))
        relative_image = cv2.warpPerspective(
            relative_extractor.standard_image, h, (700, 700))
        absolute_image = cv2.warpPerspective(
            absolute_extractor.standard_image, h, (700, 700))

        score_relative = compute_difference_score(
            current_image, relative_image, threshold, "relative")
        score_absolute = compute_difference_score(
            current_image, absolute_image, threshold, "absolute")

        # Count for moov and fix on relative difference
        if score_relative >= threshold:
            relative_fix_time = 0
            relative_moov_time = relative_moov_time + diff_time
        else:
            relative_moov_time = 0
            relative_fix_time = relative_fix_time + diff_time

        # Count for moov on absolute difference
        if score_absolute >= threshold:
            absolute_moov_time = absolute_moov_time + diff_time
        else:
            absolute_moov_time = 0

        # Count for unvalide plate sequence
        chess_plate = current_extractor.extract()

        if chess_plate == None or not chess_plate.is_valide():
            unvalide_plate_time = unvalide_plate_time + diff_time
        else:
            last_valid_plate = chess_plate
            unvalide_plate_time = 0

            # Long moov detected
            if relative_moov_time >= LM__MIN_RELATIVE_MOOV:
                long_moov_detected = True

            #  or game.board.turn == chess.BLACK
            if (absolute_moov_time > NS__MIN_ABSOLUTE_MOOV) and relative_fix_time >= NS__MIN_RELATIVE_FIX and long_moov_detected:

                if game.is_player_turn():
                    game.play_from_plate(chess_plate)

                    img_logger.log(frame)
                    cropped_logger.log(chess_plate.plate_img)

                    print("Player has played : ")
                    print(game.board)

                    result = engine.play(
                        game.board, chess.engine.Limit(time=0.1))

                    print("L'IA decide de joué le coup : ", result.move)
                    print("Vous devez reporter le coup sur le plateau !")

                else:

                    game.play_from_move(result.move, chess_plate)

                    print("Le coup de l'IA a été reporté sur le plateau :")
                    print(game.board)

                new_state(current_extractor)

        # Affichage

        rlt_color = (0, 0, 255) if score_relative >= threshold else (0, 255, 0)
        image = cv2.putText(current_image, "score rlt : " + str(score_relative), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, rlt_color, 2, cv2.LINE_AA)

        abs_color = (0, 0, 255) if score_absolute >= threshold else (0, 255, 0)
        image = cv2.putText(image, "score abs : " + str(score_absolute), (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, abs_color, 2, cv2.LINE_AA)

        image = cv2.putText(image, "rlt moov : " + str(relative_moov_time), (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "rlt fix : " + str(relative_fix_time), (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "abs moov : " + str(absolute_moov_time), (50, 250), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "unvalid : " + str(unvalide_plate_time), (50, 300), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)

        image = cv2.putText(image, "state : " + ("player" if game.is_player_turn() else "ia report"), (50, 400), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "long_moov : " + ("Oui" if long_moov_detected else "Non"), (50, 450), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("changes", image)
        # Press Q on keyboard to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
