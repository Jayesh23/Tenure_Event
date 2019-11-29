import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
	ret, img = cap.read()
	
	# img = cv2.imread('circles.png', 1)

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_range = np.array([20, 100, 100])
	upper_range = np.array([30, 255, 255])

	if(cv2.inRange(hsv, lower_range, upper_range)):
		print("Yes")

	mask = cv2.inRange(hsv, lower_range, upper_range)

	# print(mask)

	cv2.imshow('mask',mask)
	cv2.imshow('image', img)
	 
	# cv2.imshow("output", image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
 
cv2.destroyAllWindows()