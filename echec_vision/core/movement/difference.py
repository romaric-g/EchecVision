import cv2
import imutils
from core.utils.image_logger import ImageLogger


# ------------------------------------------------------------
# Permet de calculer le score de difference entre 2 images
# ------------------------------------------------------------


def compute_difference_score(original, new, min_area=1000, log_name="thresh", logger: ImageLogger = None):
    original = imutils.resize(original, height=600)
    new = imutils.resize(new, height=600)

    diff = original.copy()
    cv2.absdiff(original, new, diff)

    # converting the difference into grayscale images
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    dilated = cv2.erode(gray.copy(), None, iterations=1)

    # dilated = gray.copy()

    (T, thresh) = cv2.threshold(dilated, 10, 255, cv2.THRESH_BINARY)

    cv2.imshow(log_name, thresh)

    if logger is not None:
        logger.log(thresh)

    # now we have to find contours in the binarized image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    count = 0

    for cnt in cnts:
        rect = cv2.minAreaRect(cnt)
        width = rect[1][0]
        height = rect[1][1]

        area = width * height

        if (area >= min_area):
            count += area

    return count

# ------------------------------------------------------------
# Permet d'afficher les differences entre 2 images
# ------------------------------------------------------------


def show_difference(original, new):
    # resize the images to make them small in size. A bigger size image may take a significant time
    # more computing power and time
    original = imutils.resize(original, height=600)
    new = imutils.resize(new, height=600)

    diff = original.copy()
    cv2.absdiff(original, new, diff)

    # converting the difference into grayscale images
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    dilated = cv2.dilate(gray.copy(), None, iterations=10)

    dilated = gray.copy()

    # threshold the gray image to binary it. Anything pixel that has
    # value higher than 3 we are converting to white
    # (remember 0 is black and 255 is exact white)
    # the image is called binarised as any value lower than 3 will be 0 and
    # all of the values equal to and higher than 3 will be 255
    (T, thresh) = cv2.threshold(dilated, 20, 255, cv2.THRESH_BINARY)

    cv2.imshow("thresh", thresh)

    # now we have to find contours in the binarized image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    score = 0
    min_area = 100

    max_area = (new.shape[0] * new.shape[1]) * .9

    for c in cnts:
        # nicely fiting a bounding box to the contour
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)

        rect = cv2.minAreaRect(c)
        width = rect[1][0]
        height = rect[1][1]

        area = width * height

        if (area >= min_area) and (area <= max_area):
            score += area

        print(str(area))

    image = cv2.putText(new, str(score), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)

    # remove comments from below 2 lines if you want to
    # for viewing the image press any key to continue
    # simply write the identified changes to the disk
    cv2.imshow("changes", image)
    cv2.waitKey(0)
