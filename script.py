import cv2
import numpy as np
import os

##########################
path = '/Users/mac/Desktop/Projects/python/OMR_MARKS_CALCULATOR/test.jpg'  # This joins the current directory with the file name
widthImg = 700
heightImg = 700
############################
# Load the image
img = cv2.imread(path)
imgContour=img.copy()
imgAllContour = img.copy()
imgbiggestcontour=img.copy()
imggradepoint=img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

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

def reorder(myPoints):
    myPoints=myPoints.reshape((4,2))
    add=myPoints.sum(1)
    myPointsnew=np.zeros((4,1,2),np.int32)
    myPointsnew[0]=myPoints[np.argmin(add)]
    myPointsnew[3]=myPoints[np.argmax(add)]
    diff= np.diff(myPoints,axis=1)
    myPointsnew[1]=myPoints[np.argmin(diff)]
    myPointsnew[2]=myPoints[np.argmax(diff)]
    return myPointsnew

def getCornerPoints(contour):
    pari = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * pari, True)
    return approx


# FINDING ALL CONTOURS
contours, hiergraphy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 10)


rectCon=rectContours(contours)
biggestcontour=getCornerPoints(rectCon[0])
gradepoint=getCornerPoints(rectCon[2])

if biggestcontour.size != 0 and gradepoint.size !=0:
    cv2.drawContours(imgbiggestcontour, biggestcontour, -1, (0, 255, 0), 20)
    cv2.drawContours(imgbiggestcontour, gradepoint, -1, (0, 0, 255), 20)
    biggestcontour=reorder(biggestcontour)
    gradepoint=reorder(gradepoint)

    pt1=np.float32(biggestcontour)
    pt2=np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
    matrix=cv2.getPerspectiveTransform(pt1,pt2)
    imgWrapedColored=cv2.warpPerspective(img,matrix,(widthImg,heightImg))

    pt1=np.float32(gradepoint)
    pt2=np.float32([[0,0],[325,0],[0,150],[325,150]])
    matrixG=cv2.getPerspectiveTransform(pt1,pt2)
    imgGradeWrapedColored=cv2.warpPerspective(img,matrixG,(325,150))


    
    




cv2.imshow("Image",img)
cv2.imshow("Image1",imgGray)
cv2.imshow("Image2",imgCanny)
cv2.imshow("Image3",img)
cv2.imshow("All Contours",imgContour)
cv2.imshow("Biggest contour",imgbiggestcontour)
cv2.imshow("wrap",imgWrapedColored)
cv2.imshow("grade wrap",imgGradeWrapedColored)

cv2.waitKey(0)