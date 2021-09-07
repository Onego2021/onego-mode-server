import cv2
import numpy as np

def contour_img(src):
    dst = cv2.resize(src, dsize=(4242,3000), interpolation=cv2.INTER_AREA)
    mode = cv2.RETR_CCOMP 
    method = cv2.CHAIN_APPROX_SIMPLE

    # gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(dst, 220, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, mode, method)

    slot_list = []
    toSort = []
    ctrs = []
    ct = 0

    for cnt in contours:
        x, y, width, height = cv2.boundingRect(cnt)
        var = (x, y, cnt)
        toSort.append(var)

    toSort = sorted(toSort, key = lambda x : (x[1], x[0]))

    for var in toSort:
        ctrs.append(var[2])

    for cnt in ctrs:
        x, y, width, height = cv2.boundingRect(cnt)
        area = width*height
        if area > 20000 and area < 50000:
            #cv2.drawContours(dst, [cnt], 0, (255,0,0), 5)
            cut_slot = dst[y:y+height, x:x+width].copy()
            cut_slot = cv2.resize(cut_slot, dsize=(185, 167))
            #After reshpe (167,185), sort from top left to bottom right - maybe have to be fixed
            slot_list.append(cut_slot)
            #count the number of slots
            ct += 1
        #print(x, y, width, height)

    #print(ct)
    #slot_list.reverse()


    #Show each slot
    cnt = 0
    path_list = []
    path_row = []
    for slot in slot_list:
        path = "/home/kobot-10/Project/model-server/input/manuscript_contour/slot"+str(cnt)+".jpg"
        cv2.imwrite(path, slot)
        cnt +=1
        path_row.append(path)
        if(cnt %20 == 0):
            path_list.append(path_row)
            path_row = []


    print(path_list)
    return path_list

    """
    #Show overall image
    cv2.imshow('thresh', thresh)
    cv2.imshow('result', dst)
    cv2.waitKey()
    cv2.destroyAllWindows()
    """