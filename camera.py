import gripper
import cv2
import numpy as np
from PIL import Image
grip = gripper.Gripper()
#import findCenter as fc
from robot import Robot
import time


# Kýrmýzý rengin HSV aralýðýný tanýmla
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

    # Yeþil rengin HSV aralýðýný tanýmla
lower_green = np.array([40, 100, 100])
upper_green = np.array([80, 255, 255])

    # Siyah rengin HSV aralýðýný tanýmla
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 71])


def find_obj(img,renk,robot):
    global dx,cisim_zaman,grip
    # Görüntüyü BGR renk uzayýndan HSV renk uzayýna dönüþtür
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    

    # Kýrmýzý, yeþil ve siyah renkleri tespit etmek için maskelemeleri yap
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    black_mask = cv2.inRange(hsv, lower_black, upper_black)

    # Kýrmýzý, yeþil ve siyah renk maskelerini birleþtir
    mask = cv2.bitwise_or(red_mask1, red_mask2)
    # mask = cv2.bitwise_or(mask, green_mask)
    #mask = cv2.bitwise_or(mask, black_mask)

    # Orijinal görüntü üzerinde sadece kýrmýzý, yeþil ve siyah renkleri göster
    if renk==1:#red
        mask = cv2.bitwise_or(red_mask1, red_mask2)
    elif renk==2:
        mask = green_mask
    elif renk==3:
        mask = black_mask
    # Konturlarý bul
    result = cv2.bitwise_and(img, img, mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    tamam=False
    renk_bul=False

    # Her bir kontür için sýnýrlayýcý kutularý (bounding box) çiz
    for contour in contours:
        area = cv2.contourArea(contour)
        
        
        # Belirli bir boyuttan büyükse sýnýrlayýcý kutuyu çiz
        if area > 1000:
            _, _, w, _ = cv2.boundingRect(contour)
            #print("width = ",w)

            if w >600 and (renk==1 or renk==2) :
                tamam=True
                grip.drop()
                time.sleep(0.5)
                robot.backward(speed=0.2)
                time.sleep(0.5)
                robot.left(speed=0.2)
                time.sleep(0.5)
                robot.stop

            cisim_zaman=0
            renk_bul=True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
            _,_,_,dx,_=findCenter(frame,[x,y,(w),(h)])
    return result,dx,renk_bul,tamam



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
        #cv2.line(imgCentered,(0,Center_height_image),(image_width,Center_height_image),(255,0,255),4)
        cv2.line(imgCentered,(Center_width_image,0 ),(Center_width_image,image_height ),(255,0,255),4)


    if len(objects) !=0:
        #print(objects)
        #x,y,w,h = objects[0]
        
        x = objects[0]
        y = objects[1]
        w = objects[2]
        h = objects[3]
        #center of first object
        cx = x+w//2
        cy = y+h//2
        
        cv2.line(imgCentered,(Center_width_image,cy),(cx,cy),(0,255,255),2)
        #cv2.line(imgCentered,(cx,Center_height_image),(cx,cy),(0,255,0),2)

        #find distance between center
        dx=Center_width_image-cx
        dy=Center_height_image-cy
    
    
    #print("cx :",cx,"cy: ",cy,"dx: ",dx,"dy: ",dy)
    return cx,cy,imgCentered,dx,dy


def Track_obj(robot,dx,var=True):
    global cisim_zaman
    if abs(dx)>250:
        if dx>0:
            #robot.left(speed=0.15)
            robot.set_motors(0.04,0.13)
        else:
            #robot.right(speed=0.15)
            robot.set_motors(0.13,0.04)
    elif abs(dx)>150:
        if dx>0:
            #robot.left(speed=0.15)
            robot.set_motors(0.06,0.12)
        else:
            #robot.right(speed=0.15)
            robot.set_motors(0.12,0.06)
    # elif yok==False:
    #     return 0
    # else:
    #     robot.forward(speed=0.20)
    elif var==True:
        robot.forward(speed=0.15)
    elif cisim_zaman>40:
        if 130>cisim_zaman>120:
            robot.forward(speed=0.15)
        else:    
            robot.left(speed=0.13)
    
    else:
        robot.stop()


dispW=960
dispH=540


#camera='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'



#camera ="nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"

camera ="nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=(fraction)120/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink drop=1"


robot = Robot()


# Kamera baðlantýsýný baþlat
kamera = cv2.VideoCapture(camera)

start_time = time.time()
frame_count = 0

cisim_zaman=0

renk=3
prev_frame_time = 0
new_frame_time = 0

while True:
    # Kameradan görüntü al
    
    dx=-1
    ret, frame = kamera.read()
    frame_count += 1
    cisim_zaman += 1



    

    
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    
    result,dx,renk_bul,tamam = find_obj(frame,renk,robot)    
            
    if tamam==True:
        renk=3


    #print(renk)
    Track_obj(robot,dx,renk_bul)
    
    grip_delay=time.time()
    if not grip.is_hold:
        if grip.state() == gripper.Gripper.MSG_IR_OK:
            grip.hold()
            renk=1
    #print("grip delay =",time.time()-grip_delay)

    # Sonuçlarý göster
    cv2.imshow("Kýrmýzý, Yeþil ve Siyah Nesneler", result)
    cv2.imshow("Orijinal Görüntü", frame)

    # 'q' tuþuna basýlýnca döngüyü sonlandýr
    if cv2.waitKey(1) & 0xFF == ord('q'):
        robot.stop()
        break

# Kamera baðlantýsýný ve pencereleri kapat
kamera.release()
cv2.destroyAllWindows()
robot.stop()
