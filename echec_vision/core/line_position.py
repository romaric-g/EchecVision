import chess
from enum import Enum

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