import chess
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
from core.movement.change_map import from_histogram, log_change_map
from core.movement.research_move import find_best_move
from core.plate.plate import Plate
from core.line_position import WHILE_LINE_POSITION as LP
from core.utils.image_logger import ImageLogger


class Game:
    white_line_position: LP = None

    def __init__(self, plate: Plate):
        self.board = chess.Board()
        self.last_plate = plate

    def is_player_turn(self):
        return self.board.turn == chess.WHITE

    def play_from_plate(self, next_plate: Plate, logger: ImageLogger = None):
        change_map = from_histogram(
            self.last_plate, next_plate)

        log_change_map(change_map, logger)

        if (self.white_line_position == None):

            move1, s1 = find_best_move(self.board, change_map, LP.FIRST_ROW)
            move2, s2 = find_best_move(self.board, change_map, LP.LAST_ROW)
            move3, s3 = find_best_move(self.board, change_map, LP.FIRST_COLUMN)
            move4, s4 = find_best_move(self.board, change_map, LP.LAST_COLUMN)

            moves = [move1, move2, move3, move4]
            scores = np.array([s1, s2, s3, s4])

            max_idx = np.argmax(scores)
            move = moves[max_idx]

            self.white_line_position = LP(max_idx+1)

            return self.play_from_move(move, next_plate)

        move, _ = find_best_move(
            self.board, change_map, self.white_line_position)

        return self.play_from_move(move, next_plate)

    def play_from_move(self, move: chess.Move, next_plate: Plate):
        self.last_plate = next_plate
        self.board.push(move)

        return move
