from flask import Flask, render_template, Response
from face_and_circle_detection_with_websocket import get_frame
import face_and_circle_detection_with_websocket
import json, threading

t1 = threading.Thread(target=face_and_circle_detection_with_websocket.run_server)
t1.start()
t2 = threading.Thread(target=face_and_circle_detection_with_websocket.main_code)
t2.start()
print("reading....")

app = Flask(__name__)
	
@app.route('/')
def index():
	return render_template('index.html')

def gen(capture):
	while True:
		# print("getting frame")
		frame = face_and_circle_detection_with_websocket.get_frame(capture)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# def gen(camera):
# 	while True:
# 		print("getting frame")
# 		frame = camera.get_frame()
# 		yield (b'--frame\r\n'
# 			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	print(face_and_circle_detection_with_websocket.capture)
	return Response(gen(face_and_circle_detection_with_websocket.capture),
					mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(use_reloader=False)
	app.run(host='127.0.0.1', port="5000", debug=True)
