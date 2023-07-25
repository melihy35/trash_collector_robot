from robot import Robot
import findCenter as fc
import time

import gripper_metal

grip = gripper_metal.Gripper()
grip.start()

while True:
    cmd=input("enter value :")

    if cmd == "hold":
        grip.hold()
        #     print("hold ok")
        # else:
        #     print("hold not ok")

    if cmd =="drop":
        grip.drop()
    if cmd =="is":
        grip.material()

    if cmd =="al":
        grip.hold()
        time.sleep(0.9)
        grip.material()
        time.sleep(3.7)
        print("******son buldu")





