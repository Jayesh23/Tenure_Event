import numpy as np
import cv2
import glob
from collections import deque
import os

whiteLower = np.array([0,0,0])
whiteUpper = np.array([255,255,255])

darkblueLower = np.array([101,136,125])
darkblueUpper = np.array([121,184,201])

# greenLower = np.array([56,66,51])
# greenUpper = np.array([85,150,130])

greenLower = np.array([40,63,86])
greenUpper = np.array([71,145,181])

redLower = np.array([169,145,29])
redUpper = np.array([180,207,190])

yellowLower = np.array([21,137,121])
yellowUpper = np.array([36,202,191])

from collections import deque

# Define the upper and lower boundaries for a color to be considered "Blue"
# blueLower = np.array([100, 60, 60])
# blueUpper = np.array([140, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# Setup deques to store separate colors in separate arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]



bindex = 0
gindex = 0
rindex = 0
yindex = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

# (145, 255, 251)

colorIndex = 0

# Setup the Paint interface
paintWindow = np.zeros((1366,768,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)
cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Load the video
camera = cv2.VideoCapture(0)

path = os.listdir('saved/')

img_no=1
done = 0

def colour_points( hsv, img, lower_thres, upper_thres, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, colorIndex):
    
    blueMask = cv2.inRange(hsv, lower_thres, upper_thres)
    blueMask = cv2.erode(blueMask, kernel, iterations=3)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=2)

    # Find contours in the image
    (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Check to see if any contours were found
    if len(cnts) > 0:
        # Sort the contours and find the largest one -- we
        # will assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # cv2.circle(img, (int(x), int(y)), 1, (0, 255, 255), 10)
        
        # Get the moments to calculate the center of the contour (in this case Circle)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))


        if colorIndex==4:
            # if 40 <= center[0] <= 140: # Clear All

            bpoints.clear()
            gpoints.clear()
            rpoints.clear()
            ypoints.clear()
            

            bpoints = [deque(maxlen=512)]
            gpoints = [deque(maxlen=512)]
            rpoints = [deque(maxlen=512)]
            ypoints = [deque(maxlen=512)]

            bindex = 0
            gindex = 0
            rindex = 0
            yindex = 0

            paintWindow[67:,:,:] = 255

        #     elif 160 <= center[0] <= 255:
        #             colorIndex = 0 # Blue
        #     elif 275 <= center[0] <= 370:
        #             colorIndex = 1 # Green
        #     elif 390 <= center[0] <= 485:
        #             colorIndex = 2 # Red
        #     elif 505 <= center[0] <= 600:
        #             colorIndex = 3 # Yellow

        else :
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)
    # Append the next deque when no contours are detected (i.e., bottle cap reversed)
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1

    # Draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue

                # cv2.circle(img, (int(points[i][j][k - 1][0]), int(points[i][j][k - 1][1])), 1, (0, 255, 255), 10)
                # cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(img, points[i][j][k - 1], points[i][j][k], colors[i], 10)
                # print( points[i][j][k - 1][0], points[i][j][k - 1][1], points[i][j][k])
                # cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    return img


# cv2.namedWindow("Paint", cv2.WINDOW_NORMAL)          
# cv2.setWindowProperty("Paint", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
while True:

    img = cv2.imread('saved/' + str(img_no)+'.jpg')
    # img = cv2.imread('saved/26.png')
    if img is None:
        img_no+=1
        continue
    # img = cv2.resize(img, (1920, 1080))
    img = cv2.resize(img, (1366, 768))

    while True:
        # Grab the current paintWindow
        (grabbed, frame) = camera.read()
        # frame = cv2.resize(frame, (1920,1080))
        frame = cv2.resize(frame, (1366,768))
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # img = cv2.rectangle(img, (40,1), (140,65), (122,122,122), -1)
        # img = cv2.rectangle(img, (160,1), (255,65), colors[0], -1)
        # img = cv2.rectangle(img, (275,1), (370,65), colors[1], -1)
        # img = cv2.rectangle(img, (390,1), (485,65), colors[2], -1)
        # img = cv2.rectangle(img, (505,1), (600,65), colors[3], -1)
        # cv2.putText(img, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

        # Add the coloring options to the frame
        # frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
        # frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
        # frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
        # frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
        # frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
        # cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

        # Check to see if we have reached the end of the video
        if not grabbed:
            break

        img = colour_points( hsv, img, darkblueLower, darkblueUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 0)
        img = colour_points( hsv, img, greenLower, greenUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 1)
        img = colour_points( hsv, img, redLower, redUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 2)
        img = colour_points( hsv, img, yellowLower, yellowUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 3)
        # img = colour_points( hsv, img, whiteLower, whiteUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 4)

        # Determine which pixels fall within the blue boundaries and then blur the binary image
        # blueMask = cv2.inRange(hsv, blueLower, blueUpper)
        # blueMask = cv2.erode(blueMask, kernel, iterations=2)
        # blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
        # blueMask = cv2.dilate(blueMask, kernel, iterations=1)

        # # Find contours in the image
        # (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
        #     cv2.CHAIN_APPROX_SIMPLE)
        # center = None

        # # Check to see if any contours were found
        # if len(cnts) > 0:
        #     # Sort the contours and find the largest one -- we
        #     # will assume this contour correspondes to the area of the bottle cap
        #     cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        #     # Get the radius of the enclosing circle around the found contour
        #     ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        #     # Draw the circle around the contour
        #     cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        #     # cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            
        #     # Get the moments to calculate the center of the contour (in this case Circle)
        #     M = cv2.moments(cnt)
        #     center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        #     if center[1] <= 65:
        #         if 40 <= center[0] <= 140: # Clear All
        #             bpoints = [deque(maxlen=512)]
        #             gpoints = [deque(maxlen=512)]
        #             rpoints = [deque(maxlen=512)]
        #             ypoints = [deque(maxlen=512)]

        #             bindex = 0
        #             gindex = 0
        #             rindex = 0
        #             yindex = 0

        #             paintWindow[67:,:,:] = 255
        #         elif 160 <= center[0] <= 255:
        #                 colorIndex = 0 # Blue
        #         elif 275 <= center[0] <= 370:
        #                 colorIndex = 1 # Green
        #         elif 390 <= center[0] <= 485:
        #                 colorIndex = 2 # Red
        #         elif 505 <= center[0] <= 600:
        #                 colorIndex = 3 # Yellow
        #     else :
        #         if colorIndex == 0:
        #             bpoints[bindex].appendleft(center)
        #         elif colorIndex == 1:
        #             gpoints[gindex].appendleft(center)
        #         elif colorIndex == 2:
        #             rpoints[rindex].appendleft(center)
        #         elif colorIndex == 3:
        #             ypoints[yindex].appendleft(center)
        # # Append the next deque when no contours are detected (i.e., bottle cap reversed)
        # else:
        #     bpoints.append(deque(maxlen=512))
        #     bindex += 1
        #     gpoints.append(deque(maxlen=512))
        #     gindex += 1
        #     rpoints.append(deque(maxlen=512))
        #     rindex += 1
        #     ypoints.append(deque(maxlen=512))
        #     yindex += 1

        # # Draw lines of all the colors (Blue, Green, Red and Yellow)
        # points = [bpoints, gpoints, rpoints, ypoints]
        # for i in range(len(points)):
        #     for j in range(len(points[i])):
        #         for k in range(1, len(points[i][j])):
        #             if points[i][j][k - 1] is None or points[i][j][k] is None:
        #                 continue
        #             cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
        #             cv2.line(img, points[i][j][k - 1], points[i][j][k], colors[i], 2)
        #             cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        # Show the frame and the paintWindow image
        cv2.namedWindow("Paint", cv2.WND_PROP_FULLSCREEN)          
        cv2.setWindowProperty("Paint", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Paint",img)
        cv2.imshow("Tracking", frame)
        # cv2.imshow("Paint", paintWindow)

        # If the 'q' key is pressed, stop the loop


        k = cv2.waitKey(5) & 0xFF

        if k == ord('s'):
            img_no+=1
            # print("s", img_no)
            if img_no==len(path)+1:
                img_no=1
            img = colour_points( hsv, img, whiteLower, whiteUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 4)
            break
        
        if k == ord('a'):
            img_no-=1
            # print("a", img_no)
            if img_no==0:
                img_no=len(path)
            img = colour_points( hsv, img, whiteLower, whiteUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 4)
            break


        if k == ord('d'):
            img = colour_points( hsv, img, whiteLower, whiteUpper, bpoints, bindex, gpoints, gindex, rpoints, rindex, ypoints, yindex, 4)
            break

        if k == ord("q"):
            done = 1
            # print("q", img_no)
            # break
            break

        

        
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break

    if done:
        break

    # print(img_no)

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()