import cv2
import numpy as np
import os

##########################
path = '/Users/mac/Desktop/Projects/python/OMR_MARKS_CALCULATOR/test.jpg'  # This joins the current directory with the file name
widthImg = 700
heightImg = 700
############################
def rectContours(contours):
    rectContours = []
    for i in contours:
        area = cv2.contourArea(i)
        
        if area > 50:
            print("area:", area)
            pari = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * pari, True)
            print(len(approx))
            if len(approx) == 4:
                rectContours.append(i)
    rectContours = sorted(rectContours, key=cv2.contourArea, reverse=True)
    return rectContours

# Load the image
img = cv2.imread(path)
imgContour=img.copy()
imgAllContour = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

def getCornerPoints(contour):
    pari = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * pari, True)
    return approx


# FINDING ALL CONTOURS
contours, hiergraphy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 10)


rectCon=rectContours(contours)
biggestcontour=getCornerPoints(rectCon[0])
gradepoint=getCornerPoints(rectCon[1])


cv2.imshow("Image",img)
cv2.imshow("Image1",imgGray)
cv2.imshow("Image2",imgCanny)
cv2.imshow("Image3",img)
cv2.imshow("All Contours",imgContour)
cv2.waitKey(0)