import numpy as np
import cv2
from core.plate.plate import Plate
from core.utils.image_logger import ImageLogger


def log_change_map(change_map, logger: ImageLogger = None):

    if logger is None:
        return

    image = (change_map / np.max(change_map)) * 255
    logger.log(image)


def from_histogram(last_plate: Plate, next_plate: Plate):

    values = np.zeros((8, 8))

    plate1 = last_plate
    plate2 = next_plate

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

            hist1, _ = np.histogram(array1.ravel(), 8, [0, 256])
            hist2, _ = np.histogram(array2.ravel(), 8, [0, 256])

            filter = np.array([1, 1, 1])

            mask1 = np.convolve(hist1, filter)
            mask1 = mask1[1:-1]

            mask2 = np.convolve(hist2, filter)
            mask2 = mask2[1:-1]

            depassement = - hist1 - mask1 + hist2 + mask2
            depassement[depassement < 0] = 0

            score = np.sum(depassement)

            values[row, column] = score

    return values.astype(float)
