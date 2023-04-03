import chess
from enum import Enum
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
from core.movement.change_map import from_histogram
from core.line_position import get_board_square
from core.game import plt

# Permet de trouver le coup jouer le plus probable en fonction de la carte des changements


def find_best_move(board: chess.Board, change_map, white_line_position):

    ind = np.unravel_index(np.argsort(
        change_map, axis=None), change_map.shape)

    best_move = None
    best_move_score = 0

    legal_moves = board.legal_moves

    for index in reversed(range(0, len(ind[0]))):
        i = ind[0][index]
        j = ind[1][index]

        move_score = change_map[i, j]

        square = get_board_square(i, j, white_line_position)
        piece = board.piece_at(square)

        # Si il n'y a pas de piece à cette position, c'est que cette case ne peut pas être la case de depart du prochain coup
        if piece == None:
            continue

        # Si il y a une piece, mais que cette ci n'est pas au joueur, c'est que cette case ne peut pas être la case de depart du prochain coup
        if piece.color != chess.WHITE:
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
