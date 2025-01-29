import cv2
import numpy as np
import os
path = '/Users/mac/Desktop/Projects/python/OMR_MARKS_CALCULATOR/test.jpg' # This joins the current directory with the file name

widthImg = 700
heightImg = 700

# Load the image
img = cv2.imread(path)

# Check if the image is loaded correctly
if img is None:
    print("Error: Image not loaded. Check the path.")
else:
    # Process the image
    img = cv2.resize(img, (widthImg, heightImg))
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    # Display the images
    cv2.imshow("original", img)
    cv2.imshow("gray", imgGray)
    cv2.imshow("blur", imgBlur)
    cv2.imshow("canny", imgCanny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
