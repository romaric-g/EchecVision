import numpy as np
import cv2
from core.utils.image import image_resize, crop_image, get_image_center
from core.utils.math import segment_by_angle_kmeans, intersection, segmented_intersections
from core.plate.lines import get_min_max_lines


def draw_lines(img, lines, rc, gc, bc, e=1):

    if lines is None:
        return img

    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img, (x1, y1), (x2, y2), (rc, gc, bc), e)

    return img


def extract_homography(cropped_image, crop_values, segmented_lines, size):
    cropped_image_center = get_image_center(cropped_image)

    i_lines = segmented_lines[0]
    j_lines = segmented_lines[1]

    cropped_image_center_cpy = cropped_image.copy()

    cropped_image_center_cpy = draw_lines(
        cropped_image_center_cpy, i_lines, 255, 0, 0)
    cropped_image_center_cpy = draw_lines(
        cropped_image_center_cpy, j_lines, 0, 255, 0)

    cv2.imshow("cropped_image_center_cpy", cropped_image_center_cpy)

    # On utilise les points de croisements de toute les lignes sur une lignes de reference pour trouver la premiere et la derniere
    # Par default, on definit :
    # i : axe 1
    # j : axe 0
    try:
        # on inverse 0 et 1 si erreur (2 lignes paralleles)
        min_max_i_line = get_min_max_lines(
            i_lines, cropped_image_center, axis=1)
        min_max_j_line = get_min_max_lines(
            j_lines, cropped_image_center, axis=0)

    # 2 lignes paralleles => erreur
    # Si erreur, on inverse l'axe de reference pour les 2 groupes
    except:
        min_max_j_line = get_min_max_lines(
            i_lines, cropped_image_center, axis=0)
        min_max_i_line = get_min_max_lines(
            j_lines, cropped_image_center, axis=1)

    intersections = np.array(segmented_intersections(
        [min_max_i_line, min_max_j_line]))

    x, y, w, h = crop_values

    # Homographie avec les coordonnées du plateau trouvées
    src = np.array(intersections + (x, y))
    dst = np.array([[0, 0], [size, 0], [0, size], [size, size]])

    h, _ = cv2.findHomography(src, dst)

    return h
