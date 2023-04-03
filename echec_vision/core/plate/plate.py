import numpy as np
import cv2
from core.utils.image import image_resize, crop_image, image_resize_square
from core.utils.display import show_line

size = 700


class Plate:

    def __init__(self, plate_image, col_coords, row_coords, standard_image, h):
        self.standard_image = standard_image
        self.h = h

        if not is_valid_plate_info(col_coords, row_coords):
            raise Exception('invalid_plate')

        # On contruit l'objet plateau
        min_x = np.min(col_coords)
        min_y = np.min(row_coords)
        max_x = np.max(col_coords)
        max_y = np.max(row_coords)

        col_coords = col_coords - min_x
        row_coords = row_coords - min_y

        plate_image = plate_image[min_y:max_y, min_x:max_x]
        resized_plate_img = cv2.resize(
            plate_image, (800, 800), interpolation=cv2.INTER_AREA)

        col_ratio = resized_plate_img.shape[1] / plate_image.shape[1]
        row_ratio = resized_plate_img.shape[0] / plate_image.shape[0]

        resize_col_coords = (col_coords * col_ratio).astype(np.int)
        resize_row_coords = (row_coords * row_ratio).astype(np.int)

        self.plate_image = resized_plate_img
        self.col_coords = resize_col_coords
        self.row_coords = resize_row_coords

    def get_chess_plate_img(self):
        return self.plate_image.copy()

    def show(self, title="chess board"):
        final_chess_plate = self.get_chess_plate_img()

        for i in self.col_coords:
            show_line(final_chess_plate, [[i, 0]], (0, 255, 0))

        for i in self.row_coords:
            show_line(final_chess_plate, [[i, np.pi/2]], (0, 0, 255))

        cv2.imshow(title, final_chess_plate)

    def show_sobel(self):
        chess_plate_img = self.get_chess_plate_img()

        sobel_64 = cv2.Sobel(chess_plate_img, cv2.CV_64F, 1, 0, ksize=3)
        abs_64 = np.absolute(sobel_64)
        sobel_8u = np.uint8(abs_64)

        for i in self.col_coords:
            show_line(sobel_8u, [[i, 0]], (0, 255, 0))

        for i in self.row_coords:
            show_line(sobel_8u, [[i, np.pi/2]], (0, 0, 255))

        cv2.imshow('sobel_8u', sobel_8u)
        cv2.waitKey(0)

    def get_case(self, row, col):
        return self.get_case_on_img(self.plate_image, row, col)

    def get_case_on_img(self, img, row, col):
        row_start = self.row_coords[row]
        row_end = self.row_coords[row+1]
        col_start = self.col_coords[col]
        col_end = self.col_coords[col+1]

        case = img[row_start:row_end, col_start:col_end]
        return image_resize_square(case, 200)


def is_valid_plate_info(col_coords, row_coords):
    return col_coords.shape[0] == 9 and row_coords.shape[0] == 9
