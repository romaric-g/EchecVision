import numpy as np
import cv2
from core.utils.image import image_resize, crop_image, get_image_center
from core.utils.math import segment_by_angle_kmeans, intersection, segmented_intersections
from core.plate.contour import extract_contours
from core.plate.lines import extract_lines


def extract_the_significant_cropimage(image):

    significant_segmented_lines = None
    significant_cropped_image = None
    significant_crop_values = None

    contours = extract_contours(image, min_area=600, order=True)
    max_lines = 0

    for contour in contours:
        try:
            crop_values = get_crop_values(image, contour, 10)
            cropped_image = crop_image(image, crop_values)

            # # On recuper les lignes presentes dans l'image
            lines = extract_lines(cropped_image, threshold=110)

            if (len(lines) <= max_lines):
                continue

            segmented_lines = segment_by_angle_kmeans(lines)

            # Si il y a bien 2 groupes
            if len(segmented_lines) == 2:

                significant_cropped_image = cropped_image
                significant_crop_values = crop_values
                significant_segmented_lines = segmented_lines

                max_lines = len(lines)
        except:
            continue

    return significant_cropped_image, significant_crop_values, significant_segmented_lines


# Permet de recuperer les valeurs de decoupage d'une image à partir d'un contour
def get_crop_values(image, contour, padding):
    x, y, w, h = cv2.boundingRect(contour)

    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = x + min(w + padding, image.shape[0])
    h = y + min(h + padding, image.shape[1])

    return (x, y, w, h)
