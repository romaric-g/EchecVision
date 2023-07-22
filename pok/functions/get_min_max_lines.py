import cv2 as cv2
from functions.get_ref_line import *
from functions.intersection import *

# Recuperer la ligne la plus à gauche/basse et la plus à droite/haute
def get_min_max_lines(lines, center, axis=0):
    ref_line = get_ref_line(axis, center)
    
    max_point = -99999999
    min_point = 99999999 
    
    for line in lines:
        coord = intersection(ref_line, line)
        point = coord[0][axis]

        if point > max_point:
            max_point = point
            max_line = line
        if point < min_point:
            min_point = point
            min_line = line
    
    return [min_line, max_line]