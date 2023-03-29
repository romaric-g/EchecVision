import os
import numpy as np
import cv2 as cv2
from get_chess_plate import *
from classes.game import *
from classes.video_capture import *
from classes.image_logger import *


def main(image_path, dataset_name):
    export_path = 'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/generated/' + dataset_name

    image_ref = cv2.imread(image_path)

    chess_plate = get_chess_plate(image_ref)
    chess_plate.show()

    chess_plate_img = chess_plate.get_chess_plate_img()

    sobel_64 = cv2.Sobel(chess_plate_img, cv2.CV_64F, 1, 0, ksize=3)
    abs_64 = np.absolute(sobel_64)
    sobel_8u = np.uint8(abs_64)

    for i in range(0, 8):
        for j in range(0, 8):
            case = chess_plate.get_case(i, j)
            case_sobel = chess_plate.get_case_on_img(sobel_8u, i, j)

            case_filename = "case_" + str(i) + "_" + str(j) + ".png"
            case_sobel_filename = "case_" + \
                str(i) + "_" + str(j) + "_sobel.png"

            cv2.imwrite(os.path.join(export_path, case_filename), case)
            cv2.imwrite(os.path.join(
                export_path, case_sobel_filename), case_sobel)

    center = tuple([int(case.shape[0]/2), int(case.shape[1]/2)])

    a = get_ref_line(0, center)
    b = get_ref_line(1, center)

    show_line(case, a, (255, 0, 0))
    show_line(case, b, (0, 255, 0))

    cv2.imshow('sobel_8u', case)
    cv2.waitKey(0)

    cv2.imwrite(os.path.join(export_path, "source.png"), image_ref)


if __name__ == '__main__':
    main('./images/sources/2.jpg', 'datasets_2')
