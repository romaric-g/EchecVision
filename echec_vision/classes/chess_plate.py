import numpy as np
import cv2 as cv2
from functions.show_line import *

class ChessPlate:
    
    def __init__(self, plate_img, x_coords, y_coords):
        self.plate_img = plate_img
        self.x_coords = x_coords
        self.y_coords = y_coords
        
    def get_chess_plate_img(self):
        return self.plate_img.copy()
    
    def show(self):
        final_chess_plate = self.get_chess_plate_img()

        for i in self.x_coords:
            show_line(final_chess_plate, [[i, 0]], (0, 255, 0))

        for i in self.y_coords:
            show_line(final_chess_plate, [[i, np.pi/2]], (0, 0, 255))
            
        cv2.imshow('chess board',final_chess_plate)
        cv2.waitKey(0)
        
    def get_case(self, i,j):
        
        x1 = self.x_coords[i]
        x2 = self.x_coords[i+1]
        y1 = self.y_coords[j]
        y2 = self.y_coords[j+1]
        
        return self.plate_img[x1:x2, y1:y2]