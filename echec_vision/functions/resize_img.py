import cv2 as cv2

def resize_img(img, size = 700):
    width = size
    height = size
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)