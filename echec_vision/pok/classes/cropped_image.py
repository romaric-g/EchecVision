
class CroppedImage():

    def __init__(self, image, x, y, w, h):
        self.image_source = image
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = image[y:y+h, x:x+w]
        self.values = (x, y, w, h)

    def get_center(self):
        return (int(self.w/2), int(self.h/2))

    def crop_like(self, image):
        return CroppedImage(image, self.x, self.y, self.w, self.h)
