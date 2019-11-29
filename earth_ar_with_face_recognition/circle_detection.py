import cv2
import time
import math
import numpy as np

capture = cv2.VideoCapture(0)
# print capture.get(cv2.CAP_PROP_FPS)

t = 100
w = 640.0

last = 0
while True:
        ret, image = capture.read()
        img_height, img_width, depth = image.shape
        scale = w / img_width
        h = img_height * scale
        image = cv2.resize(image, (0,0), fx=scale, fy=scale)

        # Apply filters
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blured = cv2.medianBlur(grey, 9)

        grey_image = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)

        cv2.imshow('Image previews', grey_image)

        sc = 1
        md = 3
        at = 40
        circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, 1.4, 100)
        # circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, sc, md, t, at)
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")


         
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(image, (x, y), r, (0, 255, 0), 2)
                # cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
     
        # show the output image 
        cv2.imshow("output", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break