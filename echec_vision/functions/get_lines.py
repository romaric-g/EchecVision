import numpy as np
import cv2 as cv2

def get_lines(img, threshold = 120):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 150, 240, apertureSize=3)
    return cv2.HoughLines(edges, 1, np.pi/180, threshold)

