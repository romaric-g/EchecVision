import os
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
from get_chess_plate import *

def main(image_path='./images/sources/2.jpg'):
    chess_plates_img_path = [
        './images/sources/1.jpg',
        './images/sources/2.jpg',
        './images/sources/3.jpg',
        './images/sources/4.jpg',
        './images/sources/5.jpg',
        './images/sources/6.jpg',
        './images/sources/7.jpg',
        './images/sources/8.jpg',
        './images/sources/9.jpg',
        './images/sources/10.jpg',
        './images/sources/11.jpg',
        './images/sources/12.jpg',
        './images/sources/13.jpg',
    ]

    export_path = 'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/generated/datasets_2'

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
            case_sobel_filename = "case_" + str(i) + "_" + str(j) + "_sobel.png"

            cv2.imwrite(os.path.join(export_path, case_filename), case)
            cv2.imwrite(os.path.join(export_path, case_sobel_filename), case_sobel)

            #center = tuple([int(case.shape[0]/2), int(case.shape[1]/2)])

            #a = get_ref_line(0, center)
            #b = get_ref_line(1, center)

            # show_line(case,a,(255,0,0))
            # show_line(case,b,(0,255,0))

            # cv2.imshow('sobel_8u',case)
            # cv2.waitKey(0)

    cv2.imwrite(os.path.join(export_path, "source.png"), image_ref)

if __name__ == "__main__":
    main("C:/Users/Romaric/chess_data/render/train/0002.png")
    
# W : White
# B : Black

# -1 : Empty
# 1 : Pawn
# 2 : Knight
# 3 : Bishop
# 4 : Rook
# 5 : Queen
# 6 : King
