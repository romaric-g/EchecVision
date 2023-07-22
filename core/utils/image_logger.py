import os
import numpy as np
import cv2 as cv2


class ImageLogger():

    def __init__(self, export_path, suffix=None, start_index=0) -> None:
        self.index = start_index
        self.export_path = export_path
        self.suffix = suffix

    def log(self, image):
        name = str(self.index)

        if self.suffix != None:
            name = name + '_' + self.suffix

        cv2.imwrite(os.path.join(self.export_path, f'{name}.png'), image)

        self.index = self.index + 1
