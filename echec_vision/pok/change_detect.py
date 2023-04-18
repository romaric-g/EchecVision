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


if __name__ == "__main__0":
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

            a = cv2.warpPerspective(
                last_extractor.standard_image, *h, (700, 700))
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


if __name__ == "__main__":
    url = "Vidéo partie échec.mp4"
    cap = cv2.VideoCapture(url)

    # GLOBAL
    extractors = list()

    # CONFIG
    relative_depth = 5
    size = 700
    threshold = 1000

    # STATE
    state = -1
    state_extractor = None
    last_valid_extractor = None
    long_moov_detected = False

    # COUNT
    relative_moov_sq = 0
    relative_fix_sq = 0
    absolute_moov_sq = 0
    unvalide_plate_sq = 0

    def next_state(extractor):
        global state, long_moov_detected, state_extractor, relative_moov_sq, relative_fix_sq, absolute_moov_sq, unvalide_plate_sq
        state = state + 1
        state_extractor = extractor
        long_moov_detected = False

        relative_moov_sq = 0
        relative_fix_sq = 0
        absolute_moov_sq = 0
        unvalide_plate_sq = 0

    def push_extractor(extractor):
        if len(extractors) >= relative_depth:
            extractors.pop(0)
        extractors.append(extractor)

    a = 0

    while(cap.isOpened()):
        _, frame = cap.read()

        if frame is None:
            continue

        a = a + 1

        if a < 200:
            continue

        # Periode de setup
        if state == -1:
            extractor = ChessBoardExtractor(frame)
            push_extractor(extractor)

            if extractor.extract().is_valide():
                state = 0
                state_extractor = extractor
                last_valid_extractor = extractor

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
            relative_fix_sq = 0
            relative_moov_sq = relative_moov_sq + 1
        else:
            relative_moov_sq = 0
            relative_fix_sq = relative_fix_sq + 1

        # Count for moov on absolute difference
        if score_absolute >= threshold:
            absolute_moov_sq = absolute_moov_sq + 1
        else:
            absolute_moov_sq = 0

        # Count for unvalide plate sequence
        chess_plate = current_extractor.extract()

        if not chess_plate.is_valide():
            unvalide_plate_sq = unvalide_plate_sq + 1
        else:
            last_valid_plate = chess_plate
            unvalide_plate_sq = 0

        # Long moov detected
        if relative_moov_sq >= 10:
            long_moov_detected = True

        if (absolute_moov_sq > 20 or not state % 2 == 0) and relative_fix_sq >= 10 and unvalide_plate_sq < 5 and long_moov_detected:
            next_state(current_extractor)

        rlt_color = (0, 0, 255) if score_relative >= threshold else (0, 255, 0)
        image = cv2.putText(current_image, "score rlt : " + str(score_relative), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, rlt_color, 2, cv2.LINE_AA)

        abs_color = (0, 0, 255) if score_absolute >= threshold else (0, 255, 0)
        image = cv2.putText(image, "score abs : " + str(score_absolute), (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, abs_color, 2, cv2.LINE_AA)

        image = cv2.putText(image, "rlt moov : " + str(relative_moov_sq), (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "rlt fix : " + str(relative_fix_sq), (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "abs moov : " + str(absolute_moov_sq), (50, 250), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "unvalid : " + str(unvalide_plate_sq), (50, 300), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)

        image = cv2.putText(image, "state : " + str(state), (50, 400), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "long_moov : " + ("Oui" if long_moov_detected else "Non"), (50, 450), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2, cv2.LINE_AA)

        # remove comments from below 2 lines if you want to
        # for viewing the image press any key to continue
        # simply write the identified changes to the disk
        cv2.imshow("changes", image)
        cv2.waitKey(1)


if __name__ == "__main__0":

    # Pair : Blanc, Impaire : Noir
    state = "5"
    state_extractor = None
    long_moov_detected = False
    last_valid_plate = None

    extractors = []  # array size < i

    relative_moov_sq = 0
    relative_fix_sq = 0

    absolute_moov_sq = 0

    unvalide_plate_sq = 0

    images = []
    n = 0

    for image in images:

        current_extractor = ChessBoardExtractor(frame)
        relative_extractor = extractors[0]
        absolute_extractor = state_extractor

        h = relative_extractor.h

        current_image = cv2.warpPerspective(
            current_extractor.standard_image, *h, (size, size))
        relative_image = cv2.warpPerspective(
            relative_extractor.standard_image, *h, (size, size))
        absolute_image = cv2.warpPerspective(
            absolute_extractor.standard_image, *h, (size, size))

        score_relative = compute_difference_score(
            current_image, relative_image)
        score_absolute = compute_difference_score(
            current_image, absolute_image)

        # Count for moov and fix on relative difference
        if score_relative > threshold:
            relative_fix_sq = 0
            relative_moov_sq = relative_moov_sq + 1
        else:
            relative_image = 0
            relative_fix_sq = relative_fix_sq + 1

        # Count for moov on absolute difference
        if score_absolute > threshold:
            absolute_moov_sq = absolute_moov_sq + 1
        else:
            absolute_moov_sq = 0

        # Count for unvalide plate sequence
        chess_plate = current_extractor.extract()

        if not chess_plate.is_valide():
            unvalide_plate_sq = unvalide_plate_sq + 1
        else:
            last_valid_plate = chess_plate
            unvalide_plate_sq = 0

        # Long moov detected
        if relative_moov_sq >= 10:
            long_moov_detected = True

        if absolute_moov_sq > 20 and relative_fix_sq >= 5 and unvalide_plate_sq < 5:
            state = state + 1

        n = n + 1
