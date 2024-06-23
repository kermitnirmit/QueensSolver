import cv2 as cv
img = cv.imread("/Users/nirmitshah/Desktop/IMG_8038.PNG")
cv.imshow("Display window", img)
k = cv.waitKey(0)