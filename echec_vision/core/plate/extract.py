import numpy as np
import cv2
from core.utils.image import image_resize, crop_image, get_image_center
from core.utils.math import segment_by_angle_kmeans, intersection, segmented_intersections
from core.plate.research import extract_the_significant_cropimage
from core.plate.homography import extract_homography
from core.plate.lines import extract_lines, extract_points_from_lines
from core.plate.points import extract_valid_points
from core.plate.plate import Plate


def extract_plate(standard_image):
    size = standard_image.shape[0]

    cropped_image, crop_values, segmented_lines = extract_the_significant_cropimage(
        standard_image)

    if cropped_image is None:
        return None

    h = extract_homography(cropped_image, crop_values, segmented_lines, size)
    plate_image = cv2.warpPerspective(standard_image, h, (size, size))

    # On recherche des lignes dans la nouvelle image
    lines = extract_lines(plate_image, threshold=110)
    segmented_lines = segment_by_angle_kmeans(lines)

    if len(segmented_lines) < 2:
        return None

    col_coords, row_coords = extract_valid_points(plate_image, segmented_lines)

    try:
        return Plate(plate_image, col_coords, row_coords, standard_image=standard_image, h=h)
    except:
        return None
