from robot import Robot
import findCenter as fc
import time

import gripper

grip = gripper.Gripper()

while True:
    cmd=input("enter value :")

    if cmd == "hold":
        if grip.hold():
            print("hold ok")
        else:
            print("hold not ok")

    if cmd =="drop":
        grip.drop()
    if cmd=="state":
        print(grip.state()) 




