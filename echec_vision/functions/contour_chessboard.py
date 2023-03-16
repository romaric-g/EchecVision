
import cv2 as cv2
from classes.cropped_image import *
from functions.get_max_contour import *
from functions.get_lines import *
from functions.segment_by_angle_kmeans import *


def get_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_median = cv2.medianBlur(gray, 7)
    img_median = cv2.dilate(img_median, None, iterations=3)
    img_median = cv2.erode(img_median, None, iterations=3)

    # valeur à choisir avec precaution
    ret, threshold_img = cv2.threshold(img_median, 100, 255, cv2.THRESH_BINARY)
    threshold_img = cv2.bitwise_not(threshold_img)
    threshold_img = cv2.dilate(threshold_img, None, iterations=2)
    threshold_img = cv2.medianBlur(threshold_img, 9)

    contours, hierarchy = cv2.findContours(
        threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return filter_and_order_contours(contours, 600)


def get_cropped_from_contour(img, contour):
    x, y, w, h = cv2.boundingRect(contour)

    cropped_image = CroppedImage(img, x, y, w, h)

    cropped_img_ref = img[y:y+h, x:x+w]
    cropped_values = (x, y, w, h)
    cropped_center = (int(w/2), int(h/2))

    return (cropped_img_ref, cropped_values, cropped_center)


def get_cropped_object_from_contour(img, contour, padding=0):
    x, y, w, h = cv2.boundingRect(contour)

    p_x = max(x - padding, 0)
    p_y = max(y - padding, 0)
    p_w = p_x + min(w + padding, img.shape[0])
    p_h = p_y + min(h + padding, img.shape[0])

    return CroppedImage(img, p_x, p_y, p_w, p_h)


def find_best_cropped_chessboard(img, debug = False):
    contours = get_contours(img)

    max_lines = 0

    for contour in contours:
        cropped_img_ref, cropped_values, cropped_center = get_cropped_from_contour(
            img, contour)

        if debug:
            cv2.imshow("cropped_img_ref", cropped_img_ref)
            cv2.waitKey(0)

        try:
            # # On recuper les lignes presentes dans l'image
            lines = get_lines(cropped_img_ref, threshold=100)

            if (lines == None or len(lines) <= max_lines):
                continue

            segmented = segment_by_angle_kmeans(lines)

            # Si il y a bien 2 groupes
            if len(segmented) == 2:

                # On obtient 2 groupes de ligne (i et j)
                i_lines = segmented[0]
                j_lines = segmented[1]

                max_lines = len(lines)
        except:
            continue
