import numpy as np
import cv2
from core.utils.image import image_resize, crop_image, get_image_center
from core.utils.math import segment_by_angle_kmeans, intersection, segmented_intersections
from core.plate.research import extract_the_significant_cropimage
from core.plate.homography import extract_homography
from core.plate.lines import extract_lines, extract_points_from_lines
from core.plate.points import extract_valid_points
from core.plate.plate import Plate

# ------------------------------------------------------------
# Permet d'extract un plateau depuis une image
# -> Retourne None si aucune palteau n'a été trouvé
# ------------------------------------------------------------


def extract_plate(standard_image):
    size = standard_image.shape[0]

    try:
        # Extrait la sous image à partir du contour avec le plus de ligne à l'interieur
        cropped_image, crop_values, segmented_lines = extract_the_significant_cropimage(
            standard_image)

        if cropped_image is None:
            return None

        # Permet d'extraire la matrice d'homographie à partir de l'image signifiante
        h = extract_homography(
            cropped_image, crop_values, segmented_lines, size)

        # On utilise la matrice h pour créer la nouvelle image contenant le plateau avec une percepective transforme
        plate_image = cv2.warpPerspective(standard_image, h, (size, size))

        # On recherche des lignes dans la nouvelle image
        lines = extract_lines(plate_image, threshold=110)

        # On separe les lignes verticales et horizontales
        segmented_lines = segment_by_angle_kmeans(lines)

        if len(segmented_lines) < 2:
            return None

        col_coords, row_coords = extract_valid_points(
            plate_image, segmented_lines)

        return Plate(plate_image, col_coords, row_coords, standard_image=standard_image, h=h)
    except Exception as e:
        print("Error on extract : ", e)
        return None
