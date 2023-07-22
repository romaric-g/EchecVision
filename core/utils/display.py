import numpy as np
import cv2 as cv2


def show_line(img, line, color):
    arr = np.array(line[0], dtype=np.float64)
    r, theta = arr
    a = np.cos(theta)
    b = np.sin(theta)

    x0 = a*r
    y0 = b*r

    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))

    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), color, 2)
