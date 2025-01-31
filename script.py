import cv2
import numpy as np
import os

##########################
path = '/Users/mac/Desktop/Projects/python/OMR_MARKS_CALCULATOR/test.jpg'  # This joins the current directory with the file name
widthImg = 700
heightImg = 700

# Load the image
img = cv2.imread(path)

#############################
def rectContours4detail(contours):
    rectContours = []
    for i in contours:
        area = cv2.contourArea(i)
        
        if area > 5000:
            print("area:", area)
            pari = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * pari, True)
            print(len(approx))
            if len(approx) >= 4:
                rectContours.append(i)
    rectContours = sorted(rectContours, key=cv2.contourArea, reverse=True)
    return rectContours

def rectContours4marks(contours):
    rectContours = []
    for i in contours:
        area = cv2.contourArea(i)
        
        if area > 3.0 and area < 9:
            print("area:", area)
            pari = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * pari, True)
            print(len(approx))
            if len(approx) >= 4:
                rectContours.append(i)
    rectContours = sorted(rectContours, key=cv2.contourArea, reverse=True)
    return rectContours

def getCornerPoints(contour):
    pari = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * pari, True)
    return approx

# Check if the image is loaded correctly
if img is None:
    print("Error: Image not loaded. Check the path.")
    exit()

# Process the image
img = cv2.resize(img, (widthImg, heightImg))
imgContour = img.copy()
imgAllContour = img.copy()
imgRollno=img.copy()
imgSeatNo=img.copy()
imgBookletno=img.copy()
imgversion=img.copy()
imganswer1=img.copy()
imganswer2=img.copy()
imganswer3=img.copy()
imganswer4=img.copy()
imganswer5=img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

# FINDING ALL CONTOURS
contours, hiergraphy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 1)

# FIND RECTANGLES
rectContours4detail = rectContours4detail(contours)
rectContours4marks = rectContours4marks(contours)

# Get corner points for each section
rollnum = getCornerPoints(rectContours4detail[0])
seatnum = getCornerPoints(rectContours4detail[1])
bookletno = getCornerPoints(rectContours4detail[2])
version = getCornerPoints(rectContours4detail[3])
ans1 = getCornerPoints(rectContours4marks[16])
ans2 = getCornerPoints(rectContours4marks[10])
ans3 = getCornerPoints(rectContours4marks[9])
ans4 = getCornerPoints(rectContours4marks[24])
ans5 = getCornerPoints(rectContours4marks[44])
# for index, contour in enumerate(rectContours4marks):
#     # Draw the contour
#     cv2.drawContours(imgAllContour, [contour], -1, (0, 255, 0), 3)
    
#     # Get the center of the contour to place the index
#     M = cv2.moments(contour)
#     if M["m00"] != 0:
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#     else:
#         cX, cY = 0, 0

#     # Display the index at the center of the contour
#     cv2.putText(imgAllContour, str(index), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     # Print the index in the console
#     print(f"Contour index: {index}")

# Draw the contours for each section and display them
if rollnum is not None and rollnum.size != 0:
    cv2.drawContours(imgRollno, [rollnum], -1, (0, 255, 0), 20)
    cv2.imshow("Roll Number", imgRollno)
else:
    print("No valid contour found for Roll Number")

if seatnum is not None and seatnum.size != 0:
    cv2.drawContours(imgSeatNo, [seatnum], -1, (0, 255, 0), 20)
    cv2.imshow("Seat Number", imgSeatNo)
else:
    print("No valid contour found for Seat Number")

if bookletno is not None and bookletno.size != 0:
    cv2.drawContours(imgBookletno, [bookletno], -1, (0, 255, 0), 20)
    cv2.imshow("Booklet Number", imgBookletno)
else:
    print("No valid contour found for Booklet Number")

if version is not None and version.size != 0:
    cv2.drawContours(imgversion, [version], -1, (0, 255, 0), 20)
    cv2.imshow("Version", imgversion)
else:
    print("No valid contour found for Version")

if ans1 is not None and ans1.size != 0:
    cv2.drawContours(imganswer1, [ans1], -1, (0, 255, 0), 20)
    cv2.imshow("Answer 1", imganswer1)
else:
    print("No valid contour found for Answer 1")

if ans2 is not None and ans2.size != 0:
    cv2.drawContours(imganswer2, [ans2], -1, (0, 255, 0), 20)
    cv2.imshow("Answer 2", imganswer2)
else:
    print("No valid contour found for Answer 2")

if ans3 is not None and ans3.size != 0:
    cv2.drawContours(imganswer3, [ans3], -1, (0, 255, 0), 20)
    cv2.imshow("Answer 3", imganswer3)
else:
    print("No valid contour found for Answer 3")

if ans4 is not None and ans4.size != 0:
    cv2.drawContours(imganswer4, [ans4], -1, (0, 255, 0), 20)
    cv2.imshow("Answer 4", imganswer4)
else:
    print("No valid contour found for Answer 4")
if ans5 is not None and ans5.size != 0:
    cv2.drawContours(imganswer5, [ans5], -1, (0, 255, 0), 20)
    cv2.imshow("Answer 5", imganswer5)
else:
    print("No valid contour found for Answer 5")

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
listdetail=[5000,0,1,2,3]
listmark=[3,9,44,10,16,24]