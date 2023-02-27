import numpy as np
import cv2 as cv2

from get_chess_plate import *


def get_change_map(frame1, frame2):
    values = np.zeros((8, 8))

    plate1 = get_chess_plate(frame1)
    plate2 = get_chess_plate(frame2)

    plate1_img = plate1.get_chess_plate_img()
    plate2_img = plate2.get_chess_plate_img()

    plate1_img = cv2.medianBlur(plate1_img, 3)
    plate2_img = cv2.medianBlur(plate2_img, 3)

    for i in range(0, 8):
        for j in range(0, 8):

            case_to_compare = (i, j)

            case1 = plate1.get_case_on_img(plate1_img, *case_to_compare)
            case2 = plate2.get_case_on_img(plate2_img, *case_to_compare)

            case1 = cv2.cvtColor(case1, cv2.COLOR_BGR2GRAY)
            case2 = cv2.cvtColor(case2, cv2.COLOR_BGR2GRAY)

            # cv2.imshow('case 1', case1)
            # cv2.imshow('case 2', case2)

            resized1 = cv2.resize(
                case1, (10, 10), interpolation=cv2.INTER_AREA)
            resized2 = cv2.resize(
                case2, (10, 10), interpolation=cv2.INTER_AREA)

            array1 = resized1.astype(np.int16, copy=False)
            array2 = resized2.astype(np.int16, copy=False)

            array1 = array1[1:9, 1:9]
            array2 = array2[1:9, 1:9]

            diff = np.abs(np.subtract(array1, array2))

            diff = np.ones(array1.shape)[diff > 25]

            value = np.sum(diff)

            values[i, j] = value

    return values
