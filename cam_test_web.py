import cv2
import numpy as np
import nanocamera as nano
from flask import Flask, render_template, Response

app = Flask(__name__)

def empty(a):
    pass

@app.route('/')
def index():
    return render_template('index.html')

def process_frame(frame):
    imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("hue min", "hsv")
    h_max = cv2.getTrackbarPos("hue max", "hsv")
    s_min = cv2.getTrackbarPos("sat min", "hsv")
    s_max = cv2.getTrackbarPos("sat max", "hsv")
    v_min = cv2.getTrackbarPos("value min", "hsv")
    v_max = cv2.getTrackbarPos("value max", "hsv")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    return result

def generate_frames():
    camera = nano.Camera(flip=0, width=640, height=480, fps=60)
    print('CSI Camera ready? - ', camera.isReady())

    while camera.isReady():
        try:
            frame = camera.read()

            cv2.imshow("webcam",frame)
            processed_frame = process_frame(frame)

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        except KeyboardInterrupt:
            break

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    cv2.namedWindow("hsv")
    cv2.resizeWindow("hsv", 640, 240)
    cv2.createTrackbar("hue min", "hsv", 0, 179, empty)
    cv2.createTrackbar("hue max", "hsv", 179, 179, empty)
    cv2.createTrackbar("sat min", "hsv", 0, 255, empty)
    cv2.createTrackbar("sat max", "hsv", 255, 255, empty)
    cv2.createTrackbar("value min", "hsv", 0, 255, empty)
    cv2.createTrackbar("value max", "hsv", 255, 255, empty)

    app.run(host='0.0.0.0', port=5000, debug=True)

    cv2.destroyAllWindows()
