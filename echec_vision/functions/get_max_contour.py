import cv2 as cv2


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


def orders_contours(contours):
    areas = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        width = rect[1][0]
        height = rect[1][1]

        area = width * height

        areas.append(area)

    return [x for _, x in sorted(zip(areas, contours))]
