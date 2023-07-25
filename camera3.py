import gripper
import cv2
import numpy as np
from PIL import Image
grip = gripper.Gripper(port="/dev/ttyACM0")
grip.start()

#import findCenter as fc
from robot import Robot
import time
bias=40

# Kýrmýzý rengin HSV aralýðýný tanýmla
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

    # Yeþil rengin HSV aralýðýný tanýmla
lower_green = np.array([31, 84, 50])
upper_green = np.array([160, 255, 219])

    # Siyah rengin HSV aralýðýný tanýmla
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 85, 83])




def find_obj(img,renk,robot):
    global dx,cisim_zaman,grip,toplanan_count,bias
    kernel = np.ones((3, 3), np.uint8)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    if renk==3:
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        green_mask =cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.bitwise_or(red_mask1, red_mask2)
        mask= cv2.bitwise_or(mask,green_mask)
        avoidance = cv2.erode(mask, kernel)
        contours, _ = cv2.findContours(avoidance, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Belirli bir boyuttan büyükse sýnýrlayýcý kutuyu çiz
            if area > 2000 :
                x, y, w, h = cv2.boundingRect(contour)
                cisim_zaman=0
                renk_bul=False
                tamam=False
                dx=300
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # _,_,_,dx,_=findCenter(frame,[x,y,(w),(h)])
                # if dx>0:
                #     dx=-300
                #     robot.set_motors(0.45,0.2)
                #     time.sleep(0.3)
                # else:
                #     dx=300
                #     robot.set_motors(0.2,0.45)
                #     time.sleep(0.3)

                #robot.setmotors(yavas_motor,0.06)
                
        
                return frame,dx,renk_bul,tamam

    # Orijinal görüntü üzerinde sadece kýrmýzý, yeþil ve siyah renkleri göster
    if renk==1:#red
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(red_mask1, red_mask2)
    elif renk==2:
        mask = cv2.inRange(hsv, lower_green, upper_green)
    elif renk==3:
        mask = cv2.inRange(hsv, lower_black, upper_black)
    # Konturlarý bul
    
    result = cv2.bitwise_and(img, img, mask=mask)
    
    
    
    
    image = cv2.erode(mask, kernel) 
    #image = cv2.dilate(image, kernel)
    
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print("len conut",len(contours),"elapsed time 1 =",time.time()-work_delay)
    
    tamam=False
    renk_bul=False
    id=0
    max_area=-1
    # Her bir kontür için sýnýrlayýcý kutularý (bounding box) çiz
    work_delay=time.time()
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Belirli bir boyuttan büyükse sýnýrlayýcý kutuyu çiz
        if area > 750 and area>max_area:
            max_area=area
            x, y, w, h = cv2.boundingRect(contour)
            #print("width = ",w)
            
            if w >520 and (renk==1 or renk==2) :
                tamam=True
                toplanan_count+=1
                grip.drop()
                bias -=40
                time.sleep(0.5)
                robot.backward(speed=0.2)
                time.sleep(0.5)
                robot.left(speed=0.2)
                time.sleep(0.5)
                robot.stop
            #print("area of green",w)
            cisim_zaman=0
            renk_bul=True
            id+=1
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{id:.2f}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            _,_,_,dx,_=findCenter(frame,[x,y,(w),(h)])
          
    if renk!=3:
        dx=dx+bias
    
    return result,dx,renk_bul,tamam

def Cam_frame():
    _, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    pass

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
    hizli_motor=0.17
    yavas_motor=0.14
    if abs(dx)>250:
        if dx>0:
            #robot.left(speed=0.15)
            robot.set_motors(0.04,hizli_motor)
        else:
            #robot.right(speed=0.15)
            robot.set_motors(hizli_motor,0.04)
    elif abs(dx)>120:
        if dx>0:
            #robot.left(speed=0.15)
            robot.set_motors(0.06,yavas_motor)
        else:
            #robot.right(speed=0.15)
            robot.set_motors(yavas_motor,0.06)
    elif var==True:
        robot.forward(speed=0.18)
    elif cisim_zaman>3:
        if 140>cisim_zaman%300>120:
            robot.forward(speed=0.15)
        else:    
            # random_number = np.random.choice([0, 1])
            # if random_number==1:

            #     robot.left(speed=0.2)
            # else:
            #     robot.right(speed=0.2)
            robot.left(speed=0.2)
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
toplanan_count = 0

cisim_zaman=0

renk=3
prev_frame_time = 0
new_frame_time = 0

while True:
    # Kameradan görüntü al
    
    dx=-1
    ret, frame = kamera.read()
    
    cisim_zaman += 1

    
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    
    result,dx,renk_bul,tamam = find_obj(frame,renk,robot)    

    
   
    if tamam==True:
        renk=3


    #print(renk)
    #Track_obj(robot,dx,renk_bul)
    
    
    if grip.is_hold == gripper.Gripper.HOLD_NOT_OK:
        if grip.is_detected == gripper.Gripper.DET_OK:
            robot.stop()
            #renk=grip.material()
            grip.hold()
            time.sleep(0.8)
            #print("mateeril return = ",grip.material())
            #renk=grip.material()
            renk=1
            
            #send_mesage()
            #print("okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    

    # Sonuçlarý göster
    cv2.imshow("Kýrmýzý, Yeþil ve Siyah Nesneler", result)
    cv2.imshow("Orijinal Görüntü", frame)

    # 'q' tuþuna basýlýnca döngüyü sonlandýr
    if cv2.waitKey(1) & 0xFF == ord('q') :
        robot.stop()
        break
    if toplanan_count==3:
        robot.stop()
        time.sleep(1)
        toplanan_count=0
        bias=60
        break
        

# Kamera baðlantýsýný ve pencereleri kapat
kamera.release()
cv2.destroyAllWindows()
robot.stop()
grip.stop()
