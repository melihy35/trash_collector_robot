import cv2
import numpy as np
#from nanocamera.NanoCam import Camera
import nanocamera as nano

def empty(a):
    pass

if __name__ == '__main__':

    cv2.namedWindow("hsv")
    cv2.resizeWindow("hsv",640,240)
    cv2.createTrackbar("hue min","hsv",0,179,empty)
    cv2.createTrackbar("hue max","hsv",179,179,empty)
    cv2.createTrackbar("sat min","hsv",0,255,empty)
    cv2.createTrackbar("sat max","hsv",255,255,empty)
    cv2.createTrackbar("value min","hsv",0,255,empty)
    cv2.createTrackbar("value max","hsv",255,255,empty)



    # Create the Camera instance
    camera = nano.Camera(flip=0, width=1280, height=720, fps=120)
    print('CSI Camera ready? - ', camera.isReady())
    while camera.isReady():
        try:
            frame = camera.read()
            imgHsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h_min=cv2.getTrackbarPos("hue min","hsv")
            h_max=cv2.getTrackbarPos("hue max","hsv")
            s_min=cv2.getTrackbarPos("sat min","hsv")
            s_max=cv2.getTrackbarPos("sat max","hsv")
            v_min=cv2.getTrackbarPos("value min","hsv")
            v_max=cv2.getTrackbarPos("value max","hsv")


            lower=np.array([h_min,s_min,v_min])
            upper=np.array([h_max,s_max,v_max])
            mask =cv2.inRange(imgHsv,lower,upper)
            result=cv2.bitwise_and(frame,frame,mask=mask)

            # read the camera image
            
            # display the frame
            cv2.imshow("Video Frame", frame)
            cv2.imshow("result", result)
            cv2.imshow("mask", mask)
            cv2.imshow("hsv", imgHsv)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    # close the camera instance
    camera.release()

    # remove camera object
    del camera
