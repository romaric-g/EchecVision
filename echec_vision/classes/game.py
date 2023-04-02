import chess
import os
from enum import Enum
import numpy as np
import cv2 as cv2
from classes.chess_plate import *
from matplotlib import pyplot as plt
from classes.image_logger import ImageLogger


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
        # reflexion : 7-j, 7-i) ,   en test : j, 7-i
        return chess.square(j, 7-i)

    return None


imlog = 0
imlog = imlog + 1

map_logger = ImageLogger(
    'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_map', "map")


def log_change_map(change_map):
    img = (change_map / np.max(change_map)) * 255
    # plt.imshow(img, cmap='Greens', vmin=0, vmax=255)
    # plt.show()

    map_logger.log(img)


class Game:
    white_line_position: WHILE_LINE_POSITION = None
    player_color = chess.WHITE

    def __init__(self, chess_plate: ChessPlate):
        self.board = chess.Board()
        self.last_chess_plate = chess_plate

    def is_player_turn(self):
        return self.board.turn == chess.WHITE

    def play_from_plate(self, next_chess_plate: ChessPlate):
        change_map = get_change_map(
            self.last_chess_plate, next_chess_plate)

        log_change_map(change_map)

        if (self.white_line_position == None):

            move1, s1 = self.find_best_move(
                change_map, WHILE_LINE_POSITION.FIRST_ROW)
            move2, s2 = self.find_best_move(
                change_map, WHILE_LINE_POSITION.LAST_ROW)
            move3, s3 = self.find_best_move(
                change_map, WHILE_LINE_POSITION.FIRST_COLUMN)
            move4, s4 = self.find_best_move(
                change_map, WHILE_LINE_POSITION.LAST_COLUMN)

            moves = [move1, move2, move3, move4]
            scores = np.array([s1, s2, s3, s4])

            max_idx = np.argmax(scores)
            move = moves[max_idx]
            score = scores[max_idx]

            self.white_line_position = WHILE_LINE_POSITION(max_idx+1)

            return self.play_from_move(move, next_chess_plate)

        move, score = self.find_best_move(
            change_map, self.white_line_position)

        return self.play_from_move(move, next_chess_plate)

    def play_from_move(self, move: chess.Move, next_chess_plate: ChessPlate):
        self.last_chess_plate = next_chess_plate
        self.board.push(move)

    def find_best_move(self, change_map, white_line_position):

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


def get_change_map(last_chess_plate: ChessPlate, next_chess_plate: ChessPlate):

    values = np.zeros((8, 8))

    plate1 = last_chess_plate
    plate2 = next_chess_plate

    plate1_img = plate1.get_chess_plate_img()
    plate2_img = plate2.get_chess_plate_img()

    plate1_img = cv2.medianBlur(plate1_img, 3)
    plate2_img = cv2.medianBlur(plate2_img, 3)

    for row in range(0, 8):
        for column in range(0, 8):

            case_to_compare = (row, column)

            case1 = plate1.get_case_on_img(plate1_img, *case_to_compare)
            case2 = plate2.get_case_on_img(plate2_img, *case_to_compare)

            case1 = cv2.cvtColor(case1, cv2.COLOR_BGR2GRAY)
            case2 = cv2.cvtColor(case2, cv2.COLOR_BGR2GRAY)

            resized1 = cv2.resize(
                case1, (20, 20), interpolation=cv2.INTER_AREA)
            resized2 = cv2.resize(
                case2, (20, 20), interpolation=cv2.INTER_AREA)

            array1 = resized1.astype(np.int16, copy=False)
            array2 = resized2.astype(np.int16, copy=False)

            array1 = array1[2:17, 2:17]
            array2 = array2[2:17, 2:17]

            hist1, bins1 = np.histogram(array1.ravel(), 8, [0, 256])
            hist2, bins2 = np.histogram(array2.ravel(), 8, [0, 256])

            filter = np.array([1, 1, 1])

            mask1 = np.convolve(hist1, filter)
            mask1 = mask1[1:-1]

            mask2 = np.convolve(hist2, filter)
            mask2 = mask2[1:-1]

            diff = np.abs(np.subtract(hist1, hist2))
            commun = np.minimum(hist1, hist2)

            depassement = - hist1 - mask1 + hist2 + mask2
            depassement[depassement < 0] = 0

            score = np.sum(diff)
            score2 = np.sum(commun)
            score3 = np.sum(depassement)

            # print("---- hist1 ----")
            # print(hist1)
            # print("---- hist2 ----")
            # print(hist2)
            # print("diff", diff)
            # print("commun", commun)
            # print("commun", depassement)

            # print(bins1, bins2)

            # hist1[hist1 > 10] = 0
            # hist2[hist1 > 10] = 0

            # print("[Score]", score)
            # print("[Score 2]", score2)
            # print("[Score 3]", score3)

            # import matplotlib.pyplot as plt

            # plt.subplot(121)
            # plt.imshow(array1)

            # plt.subplot(122)
            # plt.imshow(array2)

            # plt.show()

            # print("[coords]", row, column)
            # print("[Score]", score)

            # fig, axs = plt.subplot_mosaic([
            #     ['resized1', 'resized2']
            # ], figsize=(7, 3.5))
            # axs["resized1"].imshow(array1)
            # axs["resized1"].set_title(f'Before ({row};{column})')
            # axs["resized2"].imshow(array2)
            # axs["resized2"].set_title(f'After ({row};{column})')
            # plt.show()

            values[row, column] = score3

    return values.astype(float)
