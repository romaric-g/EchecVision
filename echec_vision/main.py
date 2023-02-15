import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
from get_chess_plate import *

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
    './images/sources/14.jpg',
]

for image_path in chess_plates_img_path:
    image_ref = cv2.imread(image_path)
    chess_palte = get_chess_plate(image_ref)
    chess_palte.show()
