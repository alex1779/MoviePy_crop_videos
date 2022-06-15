# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:15:37 2021

@author: Ale
"""

import cv2


def draw_squares(img, div, line_thickness=2):
    height, width, _ = img.shape
    ph = round(height / div)
    qty_hor = div-1
    qty_ver = round(width / ph)
    # Horizontal lines
    for i in range(qty_hor):
        x1, y1 = 0, ph*(i+1)
        x2, y2 = width, ph*(i+1)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0),
                 thickness=line_thickness)
    # Vertical lines
    for i in range(qty_ver):
        x1, y1 = ph*(i+1), 0
        x2, y2 = ph*(i+1), height
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0),
                 thickness=line_thickness)
    
