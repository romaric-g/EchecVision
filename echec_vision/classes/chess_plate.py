import numpy as np
import cv2 as cv2
from functions.show_line import *
from functions.resize_img import *


class ChessPlate:

    def __init__(self, plate_img, x_coords, y_coords):

        resized_plate_img = cv2.resize(
            plate_img, (800, 800), interpolation=cv2.INTER_AREA)

        x_ratio = resized_plate_img.shape[1] / plate_img.shape[1]
        y_ratio = resized_plate_img.shape[0] / plate_img.shape[0]

        resize_x_coords = (x_coords * x_ratio).astype(np.int)
        resize_y_coords = (y_coords * y_ratio).astype(np.int)

        self.plate_img = resized_plate_img
        self.x_coords = resize_x_coords
        self.y_coords = resize_y_coords

    def get_chess_plate_img(self):
        return self.plate_img.copy()

    def show(self, title="chess board"):
        final_chess_plate = self.get_chess_plate_img()

        for i in self.x_coords:
            show_line(final_chess_plate, [[i, 0]], (0, 255, 0))

        for i in self.y_coords:
            show_line(final_chess_plate, [[i, np.pi/2]], (0, 0, 255))

        cv2.imshow(title, final_chess_plate)

    def show_sobel(self):
        chess_plate_img = self.get_chess_plate_img()

        sobel_64 = cv2.Sobel(chess_plate_img, cv2.CV_64F, 1, 0, ksize=3)
        abs_64 = np.absolute(sobel_64)
        sobel_8u = np.uint8(abs_64)

        for i in self.x_coords:
            show_line(sobel_8u, [[i, 0]], (0, 255, 0))

        for i in self.y_coords:
            show_line(sobel_8u, [[i, np.pi/2]], (0, 0, 255))

        cv2.imshow('sobel_8u', sobel_8u)
        cv2.waitKey(0)

    def get_case(self, i, j):
        return self.get_case_on_img(self.plate_img, i, j)

    def get_case_on_img(self, img, i, j):
        x1 = self.x_coords[i]
        x2 = self.x_coords[i+1]
        y1 = self.y_coords[j]
        y2 = self.y_coords[j+1]

        case = img[x1:x2, y1:y2]
        return resize_img(case, 200)
