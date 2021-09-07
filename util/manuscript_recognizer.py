import numpy as np
import argparse
import os
import imutils
import cv2
from skimage.segmentation import clear_border
from util.manuscript_scanner import manuscript_scanner
from util.manuscript_contour import contour_img
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from onego_recognizer.demo import start_model
def extract_korean(cell):

    thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    print("1")
    cv2.imshow("Cell Thresh", thresh)
    cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    print(c.size)
    cv2.drawContours(mask, [c], 0, 255, 0)

    digit = cv2.bitwise_and(thresh, thresh, mask=mask)

    cv2.imshow("Digit", digit)
    cv2.waitKey(0)

    return digit

def start_recognize(path):
    img = manuscript_scanner(path)
    slot_list = contour_img(img)

    # Initialize our 10x20 Manuscript Paper
    manuscript = np.zeros((10, 20), dtype="U4")
    print(img.shape)
    stepX = img.shape[1]/20
    print(stepX)
    stepY = img.shape[0]/10
    print(stepY)
    manuscript_cellLocs = []
    print(slot_list)

    return start_model()

    '''
    for y in range(0, 10):
        row = []
        for x in range(0, 20):
            startX = int(x * stepX)
            startY = int(y * stepY)
            endX = int((x + 1) * stepX)
            endY = int((y + 1) * stepY)

            row.append((startX, startY, endX, endY))
            cell = img[startY:endY, startX:endX]
            korean = extract_korean(cell)

            if korean is not None:
                roi = cv2.resize(korean, (28,28))
                roi = roi.astype("float") / 255.0
        manuscript_cellLocs.append(row)

    print(manuscript)
    k = extract_korean(img)
    '''

