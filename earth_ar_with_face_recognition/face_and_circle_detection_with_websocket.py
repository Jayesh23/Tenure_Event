import cv2
import time
import math
import numpy as np
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import threading
import json
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import pandas as pd

data_value = pd.read_csv("greeting.csv")

server = None
clients = []
capture = None

print("[INFO] loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
# writer = None
time.sleep(2.0)

# print capture.get(cv2.CAP_PROP_FPS)

class SimpleWSServer(WebSocket):
    def handleConnected(self):
        clients.append(self)

    def handleClose(self):
        clients.remove(self)


def run_server():
    global server
    server = SimpleWebSocketServer('', 9000, SimpleWSServer,
                                   selectInterval=(1000.0 / 60) / 1000)
    print("run_server")
    server.serveforever()

# t = threading.Thread(target=run_server)
# t.start()


# capture = cv2.VideoCapture(0)

def get_frame(capture):
    # print("get_frame")
    success, image = capture.read()
    ret, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tobytes()

t = 100
w = 640.0

last = 0

def main_code():
    global server
    global capture
    capture = cv2.VideoCapture(0)
    
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

        # cv2.imshow('Image previews', grey_image)

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


            print(name)
            data1 = data_value[data_value["Name"]==name]["yos"].values[0]
            if data1:
                print("age : ", data1)

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
                    x = int(x)
                    y = int(y)
                    r = int(r)


                    # print("x, y, radius", x, y, r)
                    for client in clients and data1:
                        string = json.dumps({'x': float(x) / float(w), 'y': float(y) / float(h), 'radius': float(r) / float(w), 'name' : name, 'yos': data1})
                        send_data = "'".join(string.split('"'))
                        client.sendMessage(send_data)                       
                        # test = str(json.dumps({'x': float(x) / float(w), 'y': float(y) / float(h), 'radius': float(r) / float(w)}))
                        print("Data : ", send_data)
                        # client.sendMessage(test)
                        # client.sendMessage(unicode(json.dumps({'x': float(x) / float(w), 'y': float(y) / float(h), 'radius': float(r) / float(w)})))
                    

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
    server.close()