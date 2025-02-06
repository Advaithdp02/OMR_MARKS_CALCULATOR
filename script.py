import cv2
import numpy as np
import os

##########################
path = '/Users/mac/Desktop/Projects/python/OMR_MARKS_CALCULATOR/test2.jpg'  # This joins the current directory with the file name
widthImg = 700
heightImg = 700
questions,values=5,5
ans=[1, 2, 0, 2, 2]
############################
# Load the image
img = cv2.imread(path)
imgContour=img.copy()
imgFinal=img.copy()
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
            # print("area:", area)
            pari = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * pari, True)
            # print(len(approx))
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

def splitBoxes(img):
    rows=np.vsplit(img,5)
    boxes=[]
    for r in rows:
        cols=np.hsplit(r,5)
        for box in cols:
            boxes.append(box)
            cv2.imshow("split",box)
    return boxes

def showAnswers(img,myIndex,grading,ans,questions,values):
     secW=int(img.shape[1]/questions)
     secH=int(img.shape[0]/questions)

     for x in range(0,questions):
        myAns=myIndex[x]
        cX=(myAns*secW)+secW//2
        cY=(x*secH)+secH//2
        if grading[x]==1:
            myColor=(0,255,0)
        else:
            myColor=(0,0,255)
            correctAns=ans[x]
            cv2.circle(img,((correctAns*secW)+secW//2,cY),20,(0,255,0),cv2.FILLED)
        cv2.circle(img,(cX,cY),50,myColor,cv2.FILLED)
     return img


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

    ptg1=np.float32(gradepoint)
    ptg2=np.float32([[0,0],[325,0],[0,150],[325,150]])
    matrixG=cv2.getPerspectiveTransform(ptg1,ptg2)
    imgGradeWrapedColored=cv2.warpPerspective(img,matrixG,(325,150))

    imgWrapGray=cv2.cvtColor(imgWrapedColored,cv2.COLOR_BGR2GRAY)
    imgThresh=cv2.threshold(imgWrapGray,150,255,cv2.THRESH_BINARY_INV)[1]
    boxes=splitBoxes(imgThresh)
    # cv2.imshow("Test",boxes[2])
    # print(cv2.countNonZero(boxes[2]),cv2.countNonZero(boxes[1]))
    myPixelVal=np.zeros((questions,values))
    countC,countR=0,0

    for image in boxes:
        totalPixel=cv2.countNonZero(image)
        myPixelVal[countR,countC]=totalPixel
        countC+=1
        if (countC == values):
            countR+=1
            countC=0
    # print(myPixelVal)
    myIndex = []
    for x in range(questions):
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))[0]  # Get indices where max value occurs
        myIndex.append(int(myIndexVal[0]))  # Append only the first index as an integer

    print(myIndex)


    grading=[]
    for x in range(0,questions):
        if ans[x]==myIndex[x]:
            grading.append(1)
        else:
            grading.append(0)
    print(grading)

    score=(sum(grading)/questions)*100

    imgResult=imgWrapedColored.copy()
    imgRawDrawing = np.zeros_like(imgWrapedColored)
    showAnswers(imgRawDrawing,myIndex,grading,ans,questions,values)
    cv2.imshow("result",imgRawDrawing)
   
    invmatrix = cv2.getPerspectiveTransform(pt2, pt1)
    imgInWrap = cv2.warpPerspective(imgRawDrawing, invmatrix, (widthImg, heightImg))

   
    cv2.imshow("FINAL33",imgInWrap)
    

    # cv2.imshow("FINAL",imgFinal)

# cv2.imshow("Image",img)
# cv2.imshow("Image1",imgGray)
# cv2.imshow("Image2",imgCanny)
# cv2.imshow("Image3",img)
# cv2.imshow("All Contours",imgContour)
# cv2.imshow("Biggest contour",imgbiggestcontour)
# cv2.imshow("wrap",imgWrapedColored)
# cv2.imshow("grade wrap",imgGradeWrapedColored)
# cv2.imshow("grayscale",imgThresh)
cv2.waitKey(0)