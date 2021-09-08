import numpy as np
import argparse
import os
import imutils
import easyocr
import cv2
from skimage.segmentation import clear_border
from util.manuscript_scanner import four_point_transform, manuscript_scanner
from util.manuscript_contour import contour_img
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def find_manuscript(img):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img, (3,3), 11111)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2. bitwise_not(thresh)

    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    manuscriptCnt = None
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4 :
            manuscriptCnt = approx
            break

    output = img.copy()
    cv2.drawContours(output, [manuscriptCnt], -1, (0, 255, 0), 2)
    # cv2.imshow("manuscript outline", output)
    # cv2.waitKey(0)

    manuscript_paper = four_point_transform(img, manuscriptCnt.reshape(4,2))

    # cv2.imshow("manuscript Transform", manuscript_paper)
    # cv2.waitKey(0)

    return manuscript_paper

def start_recognize(path):
    # img = manuscript_scanner(path)
    # slot_list = contour_img(img)
    # Initialize our 10x20 Manuscript Paper
    image = find_manuscript(path)
    removed = image.copy()
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(removed, [c], -1, (255,255,255), 5)
    
    removed = 255 - removed
    removed = cv2.cvtColor(removed, cv2.COLOR_BGR2GRAY)
    removed = clear_border(removed)
    # cv2.imshow('removed', removed)
    # cv2.waitKey()    

    cv2.imwrite("/home/ubuntu/onego-model-server/input/manuscript_scan/"+"before_ocr"+".jpg", removed)
    
    reader = easyocr.Reader(['ko'], gpu=False)
    result_OCR = reader.readtext("/home/ubuntu/onego-model-server/input/manuscript_scan/"+"before_ocr"+".jpg")

    result = ''
    for i in result_OCR:
        result += i[1]

    result = result.replace(' |', '')
    result = result.replace('  ', ' ')
    result = result.replace('_', '')
    result = result.replace('|', '')
    result = result.replace('[', '')
    result = result.replace(']', '')
    result = result.replace('(', '')
    result = result.replace(')', '')

    print(result)

    return result
