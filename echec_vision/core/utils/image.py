import numpy as np
import cv2 as cv2

# Permet de redimensionner une image

def image_resize_square(image, size=700):
    return image_resize(image, size, size)

def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


# Permet de decouper une image
def crop_image(image, crop_values):
    x, y, w, h = crop_values
    return image[y:y+h, x:x+w]


def get_image_center(image):
    image_shape = image.shape

    # print("Shape", image_shape)
    center = np.array([image_shape[0], image_shape[1]]).astype(np.double)
    center = center / 2
    center = center.astype(np.int16)
    center = tuple(center)

    return center
