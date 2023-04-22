import cv2


def extract_contours(image, min_area, order=True):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img_median = cv2.medianBlur(gray, 7)
    img_median = cv2.dilate(img_median, None, iterations=3)
    img_median = cv2.erode(img_median, None, iterations=3)

    # valeur à choisir avec precaution
    ret, threshold_img = cv2.threshold(img_median, 100, 255, cv2.THRESH_BINARY)
    threshold_img = cv2.bitwise_not(threshold_img)
    threshold_img = cv2.dilate(threshold_img, None, iterations=2)
    threshold_img = cv2.medianBlur(threshold_img, 9)

    contours, _ = cv2.findContours(
        threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Filter and orders contours
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

    return [x for _, x in sorted(zip(areas, new_contours), key=lambda a: a[0], reverse=order)]
