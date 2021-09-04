from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import os
import sys

def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect

def four_point_transform(image, pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

def manuscript_scanner(img):

        manuscript_img = cv2.imread(img)
        ratio = manuscript_img.shape[0] / 500.0
        orign_img = manuscript_img.copy()
        manuscript_img = imutils.resize(manuscript_img, height=500)

        # Step 1 : Edge Detection
        gray = cv2.cvtColor(manuscript_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edged = cv2.Canny(gray, 75, 200)

        #        cv2.imshow("Manuscript_Img", manuscript_img)
        #        cv2.imshow("Edged_Manuscript_Img", edged)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Step 2 : Find contours of Manuscript
        contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

        for cnts in contours:
                per = cv2.arcLength(cnts, True)
                approx = cv2.approxPolyDP(cnts, 0.02 * per, True)

                if len(approx) == 4:
                        screenContours = approx
                        break
        cv2.drawContours(manuscript_img, [screenContours], -1, (0, 255, 0), 2)
        # cv2.imshow("Outline of Manuscript", manuscript_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Step 3 : 
        warped = four_point_transform(orign_img, screenContours.reshape(4, 2) * ratio)

        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset = 10, method="gaussian")
        warped = (warped > T).astype("uint8") * 255

        # cv2.imshow("Original_Manuscript", imutils.resize(orign_img, height=650))
        # cv2.imshow("Scanned_Manuscript", imutils.resize(warped, height=650))

        cv2.imwrite("C:/Users/bamin/Project/onego-model-server/input/manuscript_scan/"+str(1)+".jpg", warped)

        return warped

        
