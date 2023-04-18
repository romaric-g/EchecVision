from functions.get_ref_line import *
from functions.intersection import *


def get_lines_cross_points(lines, center, axis=0):
    ref_line = get_ref_line(axis, center)

    points = []

    for line in lines:
        coord = intersection(ref_line, line)
        point = coord[0][axis]
        points.append(point)

    return points
