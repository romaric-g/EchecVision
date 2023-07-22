import cv2 as cv2
import numpy as np


def get_max_contour(contours):
    max_find = 0

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        width = rect[1][0]
        height = rect[1][1]

        area = width * height

        if area > max_find:
            max_find = area
            max_cnt = cnt

    return max_cnt


def filter_and_order_contours(contours, min_area, order=True):
    areas = []
    new_contours = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        width = rect[1][0]
        height = rect[1][1]

        area = width * height

        if (area >= min_area):
            areas.append(area)
            new_contours.append(cnt)

    # new_contours = np.array(new_contours)
    # areas = np.array(areas)

    # if order:
    #     inds = (-areas).argsort()[:areas.size-1]
    # else:
    #     inds = areas.argsort()

    # sorted_contours = new_contours[inds]

    # a = [*sorted_contours]

    # return a
    return [x for _, x in sorted(zip(areas, new_contours), key=lambda a: a[0], reverse=order)]
