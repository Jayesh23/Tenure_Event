import cv2
import time
import math
import numpy as np
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle

print("[INFO] loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
# writer = None
time.sleep(2.0)

capture = cv2.VideoCapture(0)
# print capture.get(cv2.CAP_PROP_FPS)

t = 100
w = 640.0

last = 0
while True:
    ret, image = capture.read()

    # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # rgb = cv2.resize(image, (0,0), fx=scale, fy=scale)
    # rgb = imutils.resize(image, width=750)
    
    img_height, img_width, depth = image.shape
    scale = w / img_width
    h = img_height * scale
    image = cv2.resize(image, (0,0), fx=scale, fy=scale)
    rgb = cv2.resize(image, (0,0), fx=scale, fy=scale)

    r = image.shape[1] / float(rgb.shape[1])

    boxes = face_recognition.face_locations(rgb, model = "cnn")
    # model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # Apply filters
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.medianBlur(grey, 9)

    grey_image = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)

    cv2.imshow('Image previews', grey_image)

    sc = 1
    md = 3
    at = 40

    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
        
        # update the list of names
        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        # rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, 1.35, 100)
        # circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, sc, md, t, at)
        if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")


         
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # print("x, y, r, ", x, y, r)
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                yellow_lower = np.array([22,60,200],np.uint8)
                yellow_upper = np.array([60,255,255],np.uint8)
                yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(image, (x, y), r, (0, 255, 0), 2)
                

        # draw the predicted face name on the image
        cv2.rectangle(image, (left, top), (right, bottom),
            (0, 255, 0), 1)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 1)


    
            # cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
    # show the output image 
    cv2.imshow("output", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break