import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read an image
img = cv2.imread("src/lineroad.jpg")

height, width  = img.shape[:2]

# Define an array of endpoints of triangle
points = np.array([[int(width/2), 0], [0, height], [width, height]])
# Use fillPoly() function and give input as
# image, end points,color of polygon
# Here color of polygon will blue
cv2.fillPoly(img, pts=[points], color=(255, 0, 0))
image = cv2.rectangle(img, (0, 0), (height, width), color=(255, 0, 0))
# Displaying the image
cv2.imshow("", img)
 
# wait for the user to press any key to 
# exit window
cv2.waitKey(0)
 
# Closing all open windows
cv2.destroyAllWindows()