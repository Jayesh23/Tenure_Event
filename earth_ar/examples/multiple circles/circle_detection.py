import cv2
import time
import math
import numpy as np

capture = cv2.VideoCapture(0)
print capture.get(cv2.CAP_PROP_FPS)

t = 100
w = 640.0

last = 0
while True:
        ret, image = capture.read()
        # print("ret ",ret)
        img_height, img_width, depth = image.shape
        scale = w / img_width
        h = img_height * scale
        image = cv2.resize(image, (0,0), fx=scale, fy=scale)

        # Apply filters
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blured = cv2.medianBlur(grey, 9)

        grey_image = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)

        cv2.imshow('Image previews', image)

        sc = 1
        md = 30
        at = 40
        circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, sc, md, t, at)

        if circles is not None:
            # We care only about the first circle found.
            circle = circles[0][0]
            # if(circles[0][0].size==3):
            #     print(circles)
        if circle.size == 3:
            # print(circle.size)
            x, y, radius = int(circle[0]), int(circle[1]), int(circle[2])
            print(float(x) / float(w), float(y) / float(h), float(radius) / float(w))

            # Highlight the circle
            cv2.circle(image, (x, y), radius, (0, 0, 255), 1)
            # Draw dot in the center
            cv2.circle(image, (x, y), 1, (0, 0, 255), 1)

            # for client in clients:
            #         client.sendMessage(unicode(json.dumps({'x': float(x) / float(w), 'y': float(y) / float(h), 'radius': float(radius) / float(w)})))

        cv2.imshow('Image with detected circle', grey_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break