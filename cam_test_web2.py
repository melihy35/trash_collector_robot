import cv2
import numpy as np
#from nanocamera.NanoCam import Camera
import nanocamera as nano
from flask import Flask, render_template, Response


app = Flask(__name__)

frame=0
def empty(a):
    pass

@app.route('/')
def index():
    return render_template('index.html')

def Cam_frame():
    global frame
    _, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(Cam_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



    # Create the Camera instance0
    camera = nano.Camera(flip=0, width=640, height=480, fps=60)
    print('CSI Camera ready? - ', camera.isReady())
    while camera.isReady():
        try:
            frame = camera.read()

            # read the camera image
            
            # display the frame
            cv2.imshow("Video Frame", frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    # close the camera instance
    camera.release()

    # remove camera object
    del camera