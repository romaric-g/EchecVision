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

    return [x for _, x in sorted(zip(areas, new_contours), reverse=order)]
