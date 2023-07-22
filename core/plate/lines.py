import numpy as np
import cv2
from core.utils.image import image_resize, crop_image, get_image_center
from core.utils.math import segment_by_angle_kmeans, intersection, segmented_intersections

# ------------------------------------------------------------
# Permet de recuperer la ligne de reference pour comparer plusieurs lignes entres elles
# axis : (0 : Verticale, 1 : Hozitontale)
# center : décalager par rapport à gauche (pour un axe verticale) ou au haut (pour un axe horizontale)
# ------------------------------------------------------------


def get_ref_line(axis, center):
    if axis == 1:
        return [[center[0], 0]]
    return [[center[1], np.pi/2]]


def extract_lines(img, threshold=120):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 150, 240, apertureSize=3)
    return cv2.HoughLines(edges, 1, np.pi/180, threshold)


# Permet de trouver les lignes exterieurs à partir d'une liste
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


def extract_points_from_lines(lines, center, axis=0):
    ref_line = get_ref_line(axis, center)

    points = []

    for line in lines:
        coord = intersection(ref_line, line)
        point = coord[0][axis]
        points.append(point)

    return points
