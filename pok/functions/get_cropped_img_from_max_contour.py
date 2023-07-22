import cv2 as cv2
from functions.get_max_contour import *

def get_cropped_img_from_max_contour(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img_median = cv2.medianBlur(gray, 7)
    img_median = cv2.dilate(img_median, None, iterations = 3)
    img_median = cv2.erode(img_median, None, iterations = 3)

    ret,threshold_img = cv2.threshold(img_median,100,255,cv2.THRESH_BINARY) # valeur à choisir avec precaution
    threshold_img = cv2.bitwise_not(threshold_img)
    threshold_img = cv2.dilate(threshold_img, None, iterations = 2)
    threshold_img = cv2.medianBlur(threshold_img, 9)

    contours, hierarchy = cv2.findContours(threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    graycopy = gray.copy()
    graycopy = cv2.drawContours(graycopy, contours, -1, (0,255,0), 20)

    cv2.imshow("graycopy", graycopy)
    cv2.waitKey(0)


    max_cnt = get_max_contour(contours)

    x, y, w, h = cv2.boundingRect(max_cnt)

    cropped_img_ref = img[y:y+h, x:x+w]
    cropped_values = (x,y,w,h)
    cropped_center = (int(w/2),int(h/2))
    
    return (cropped_img_ref, cropped_values, cropped_center)
    