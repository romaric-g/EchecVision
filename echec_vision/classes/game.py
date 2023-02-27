import chess
from enum import Enum
import numpy as np
import cv2 as cv2
from classes.chess_plate import *


class WHILE_LINE_POSITION(Enum):
    FIRST_ROW = 1
    LAST_ROW = 2
    FIRST_COLUMN = 3
    LAST_COLUMN = 4


def get_board_square(i, j, while_line_position):

    if (while_line_position == WHILE_LINE_POSITION.FIRST_COLUMN):
        return chess.square(i, j)
    if (while_line_position == WHILE_LINE_POSITION.FIRST_ROW):
        return chess.square(7-j, i)
    if (while_line_position == WHILE_LINE_POSITION.LAST_COLUMN):
        return chess.square(7-i, 7-j)
    if (while_line_position == WHILE_LINE_POSITION.LAST_ROW):
        return chess.square(j, 7-i)

    return None


class Game:
    white_line_position: WHILE_LINE_POSITION = None
    player_color = chess.WHITE

    def __init__(self, chess_plate: ChessPlate):
        self.board = chess.Board()
        self.last_chess_plate = chess_plate

    def play_from_plate(self, next_chess_plate: ChessPlate):

        if (self.white_line_position == None):

            move, score = self.find_best_move(
                next_chess_plate, WHILE_LINE_POSITION.FIRST_COLUMN)

            # Va poser des problemes

            # move2, s2 = self.find_best_move(
            #     next_chess_plate, WHILE_LINE_POSITION.LAST_ROW)
            # move3, s3 = self.find_best_move(
            #     next_chess_plate, WHILE_LINE_POSITION.FIRST_COLUMN)
            # move4, s4 = self.find_best_move(
            #     next_chess_plate, WHILE_LINE_POSITION.LAST_COLUMN)

            # moves = [move1, move2, move3, move4]
            # scores = np.array([s1, s2, s3, s4])

            # max_idx = np.argmax(scores)
            # move = moves[max_idx]
            # score = scores[max_idx]

            # self.while_line_position = WHILE_LINE_POSITION(max_idx)
            self.white_line_position = WHILE_LINE_POSITION.FIRST_COLUMN

            return self.play_from_move(move, next_chess_plate)

        move, score = self.find_best_move(
            next_chess_plate, self.white_line_position)

        return self.play_from_move(move, next_chess_plate)

    def play_from_move(self, move: chess.Move, next_chess_plate: ChessPlate):

        print(move)

        self.last_chess_plate = next_chess_plate
        self.board.push(move)

    def find_best_move(self, next_chess_plate, white_line_position):

        change_map = self.get_change_map(next_chess_plate)

        ind = np.unravel_index(np.argsort(
            change_map, axis=None), change_map.shape)

        best_move = None
        best_move_score = 0

        legal_moves = self.board.legal_moves

        for index in reversed(range(0, len(ind[0]))):
            i = ind[0][index]
            j = ind[1][index]

            move_score = change_map[i, j]

            square = get_board_square(i, j, white_line_position)
            piece = self.board.piece_at(square)

            # Si il n'y a pas de piece à cette position, c'est que cette case ne peut pas être la case de depart du prochain coup
            if piece == None:
                continue

            # Si il y a une piece, mais que cette ci n'est pas au joueur, c'est que cette case ne peut pas être la case de depart du prochain coup
            if piece.color != self.player_color:
                continue

            attacked_squares = self.board.attacks(square)

            best_target_square = None
            best_target_score = 0

            for index in reversed(range(0, len(ind[0]))):
                i2 = ind[0][index]
                j2 = ind[1][index]

                square2 = get_board_square(i2, j2, white_line_position)

                for move in legal_moves:

                    if move.from_square != square:
                        continue

                    if move.to_square == square2:
                        # First find is best
                        best_target_square = move.to_square
                        best_target_score = change_map[i2, j2]
                        break

                if best_target_square != None:
                    move_score = move_score + best_target_score
                    break

            if move_score > best_move_score:
                best_move = chess.Move(square, square2)
                best_move_score = move_score

        return (best_move, best_move_score)

    def get_change_map(self, next_chess_plate: ChessPlate):

        values = np.zeros((8, 8))

        plate1 = self.last_chess_plate
        plate2 = next_chess_plate

        plate1_img = plate1.get_chess_plate_img()
        plate2_img = plate2.get_chess_plate_img()

        plate1_img = cv2.medianBlur(plate1_img, 3)
        plate2_img = cv2.medianBlur(plate2_img, 3)

        for i in range(0, 8):
            for j in range(0, 8):

                case_to_compare = (i, j)

                case1 = plate1.get_case_on_img(plate1_img, *case_to_compare)
                case2 = plate2.get_case_on_img(plate2_img, *case_to_compare)

                case1 = cv2.cvtColor(case1, cv2.COLOR_BGR2GRAY)
                case2 = cv2.cvtColor(case2, cv2.COLOR_BGR2GRAY)

                resized1 = cv2.resize(
                    case1, (10, 10), interpolation=cv2.INTER_AREA)
                resized2 = cv2.resize(
                    case2, (10, 10), interpolation=cv2.INTER_AREA)

                array1 = resized1.astype(np.int16, copy=False)
                array2 = resized2.astype(np.int16, copy=False)

                array1 = array1[1:9, 1:9]
                array2 = array2[1:9, 1:9]

                diff = np.abs(np.subtract(array1, array2))
                diff = np.ones(array1.shape)[diff > 25]
                value = np.sum(diff)

                values[i, j] = value

        return values
