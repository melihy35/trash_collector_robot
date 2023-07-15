"""
Find center module

by: Melih Yýldýrým 
JETBOT
"""

import cv2
import numpy as np
import time 

cap =cv2.VideoCapture(0)



def findCenter(imgCentered,objects,center_lines=True):
    """
    find center of object and distance with image center

    :param imgCentered: Images which we are using 
    :param objects: Object which is detected
    :return cx: x value of center of objects
    :return cy: y value of center of objects
    :return imageCentered: Image with bounding box and  
    :return dx: x value of center of image
    :return dy: y value of center of image
    """
    cx, cy = -1,-1
    dx, dy = -1,-1
    #Find image center
    image_height,image_width=imgCentered.shape[:2]
    Center_width_image= image_width//2
    Center_height_image= image_height//2
    #print("lines")
    if center_lines:
        cv2.line(imgCentered,(0,Center_height_image),(image_width,Center_height_image),(255,0,255),4)
        cv2.line(imgCentered,(Center_width_image,0 ),(Center_width_image,image_height ),(255,0,255),4)


    if len(objects) !=0:
        print(objects)
        #x,y,w,h = objects[0]
        
        x = objects[0]
        y = objects[1]
        w = objects[2]
        h = objects[3]
        #center of first object
        cx = x+w//2
        cy = y+h//2
        
        cv2.line(imgCentered,(Center_width_image,cy),(cx,cy),(0,255,0),2)
        cv2.line(imgCentered,(cx,Center_height_image),(cx,cy),(0,255,0),2)

        #find distance between center
        dx=abs(Center_width_image-cx) 
        dy=abs(Center_height_image-cy)
    
    
    print("dx :",dx,"dy: ",dy)
    return cx,cy,imgCentered,dx,dy

def Track(robot,dx):
    if abs(dx)>50:

        if dx<0:
            robot.left(speed=0.15)
        else:
            robot.right(speed=0.15)

prev_frame_time = 0
new_frame_time = 0

def put_fps(img):
    global prev_frame_time,new_frame_time
    """
    :param img: 

    :return : image with fps
    """
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    cv2.putText(img, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 255, 0), 3, cv2.LINE_AA)

    return img

def main():
    
    while True:
        succes, img = cap.read()
        img = cv2.flip(img, 1)
        bu_tespit_suresi =time.time()
        #image_finded,objects = odm.object_detecetion(img,scaleFactor=1.1,minNeighbors=4)
        print(time.time()-bu_tespit_suresi)
        #_ ,_ ,image_show,dx,dy= findCenter(image_finded,objects)
        #


        image_show = put_fps(image_show)

        cv2.imshow("bu kamera",image_show)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()