import time
import cv2
import chess
from core.plate.extract import extract_plate
from core.plate.plate import Plate
from core.movement.difference import compute_difference_score
from core.game import Game
from core.utils.image import image_resize
from core.utils.image_logger import ImageLogger


RELATIVE_DEPTH = 5
MOVE_THRESHOLD = 1000

LM__MIN_RELATIVE_MOOV = 1.5

NS__MIN_ABSOLUTE_MOOV = 2.5
NS__MIN_RELATIVE_FIX = 1.5
NS__MAX_UNVALIDE_PLATE = .5

engine = chess.engine.SimpleEngine.popen_uci(
    r"C:\Users\Romaric\DataScience\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")


class MoveDetector():

    def __init__(self, log_path) -> None:
        self.game: Game = None
        self.initial_plate = None
        self.long_moov_detected = False

        self.standard_images = list()
        self.last_time = time.time()

        self.relative_moov_time = 0
        self.relative_fix_time = 0
        self.absolute_moov_time = 0

        self.image_logger = ImageLogger(log_path)
        self.cropped_logger = ImageLogger(log_path, 'cropped')
        self.map_logger = ImageLogger(log_path, 'map')

    def push_standard_image(self, plate):
        if len(self.standard_images) >= RELATIVE_DEPTH:
            self.standard_images.pop(0)
        self.standard_images.append(plate)

    def new_state(self):
        self.long_moov_detected = False

        self.relative_moov_time = 0
        self.relative_fix_time = 0
        self.absolute_moov_time = 0

    def get_diff_time(self):
        now = time.time()
        diff_time = now - self.last_time
        self.last_time = now

        return diff_time

    def next_frame(self, frame, debug=False):

        standard_image = image_resize(frame, height=700)
        current_plate = extract_plate(standard_image)

        self.push_standard_image(standard_image)

        score_relative = -1
        score_absolute = -1

        if self.game == None:
            if current_plate != None:
                self.initial_plate = current_plate
                self.game = Game(self.initial_plate)

                # Log
                self.image_logger.log(self.initial_plate.standard_image)
                self.cropped_logger.log(self.initial_plate.plate_image)
        else:
            # Si la mise en place a déjà été faite
            diff_time = self.get_diff_time()

            relative_standard_image: Plate = self.standard_images[0]
            absolute_plate = self.game.last_plate

            h = self.initial_plate.h

            current_plate_image = cv2.warpPerspective(
                standard_image, h, (700, 700))
            relative_plate_image = cv2.warpPerspective(
                relative_standard_image, h, (700, 700))
            absolute_plate_image = cv2.warpPerspective(
                absolute_plate.standard_image, h, (700, 700))

            score_relative = compute_difference_score(
                current_plate_image, relative_plate_image, MOVE_THRESHOLD, "relative")
            score_absolute = compute_difference_score(
                current_plate_image, absolute_plate_image, MOVE_THRESHOLD, "absolute")

            # Count for moov and fix on relative difference
            if score_relative >= MOVE_THRESHOLD:
                self.relative_fix_time = 0
                self.relative_moov_time = self.relative_moov_time + diff_time
            else:
                self.relative_moov_time = 0
                self.relative_fix_time = self.relative_fix_time + diff_time

            # Count for moov on absolute difference
            if score_absolute >= MOVE_THRESHOLD:
                self.absolute_moov_time = self.absolute_moov_time + diff_time
            else:
                self.absolute_moov_time = 0

            # Count for unvalide plate sequence
            if current_plate != None:
                # Long moov detected
                if self.relative_moov_time >= LM__MIN_RELATIVE_MOOV:
                    self.long_moov_detected = True

                # cv2.imshow("current_plate", current_plate.plate_img)

                #  or game.board.turn == chess.BLACK
                if (self.absolute_moov_time > NS__MIN_ABSOLUTE_MOOV) and self.relative_fix_time >= NS__MIN_RELATIVE_FIX and self.long_moov_detected:

                    # Log
                    self.image_logger.log(standard_image)
                    self.cropped_logger.log(current_plate_image)

                    if self.game.is_player_turn():
                        self.game.play_from_plate(
                            current_plate, self.map_logger)

                        print("Player has played : ")
                        print(self.game.board)

                        self.result = engine.play(
                            self.game.board, chess.engine.Limit(time=0.1))

                        print("L'IA decide de joué le coup : ", self.result.move)
                        print("Vous devez reporter le coup sur le plateau !")

                    else:
                        self.game.play_from_move(
                            self.result.move, current_plate)

                        print("Le coup de l'IA a été reporté sur le plateau :")
                        print(self.game.board)

                    self.new_state()

        if debug:
            cv2.imshow("detector", self.get_debug_image(
                standard_image, score_relative, score_absolute))

    def get_debug_image(self, image, score_relative, score_absolute):

        image = image.copy()
        # Affichage

        rlt_color = (0, 0, 255) if score_relative >= MOVE_THRESHOLD else (
            0, 255, 0)
        image = cv2.putText(image, "score rlt : " + str(score_relative), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, rlt_color, 2, cv2.LINE_AA)

        abs_color = (0, 0, 255) if score_absolute >= MOVE_THRESHOLD else (
            0, 255, 0)
        image = cv2.putText(image, "score abs : " + str(score_absolute), (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, abs_color, 2, cv2.LINE_AA)

        image = cv2.putText(image, "rlt moov : " + str(self.relative_moov_time), (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "rlt fix : " + str(self.relative_fix_time), (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "abs moov : " + str(self.absolute_moov_time), (50, 250), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)

        image = cv2.putText(image, "state : " + ("player" if self.game.is_player_turn() else "ia report"), (50, 400), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "long_moov : " + ("Oui" if self.long_moov_detected else "Non"), (50, 450), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2, cv2.LINE_AA)

        return image
