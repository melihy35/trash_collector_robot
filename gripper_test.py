import serial as ser
from time import sleep
from gripper import Gripper
'''
arduino = ser.Serial(port="COM15", baudrate=9600, timeout=0.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    sleep(0.05)
    data = arduino.readline()
    return data


while True:
    num = input("Enter a number: ")     # Taking input from user
    value = write_read(num)
    print(value)    # printing the value
'''


gripper = Gripper(port="/dev/ttyUSB0")
gripper.start()
while True:
    cmd = input("Enter a command: ")     # Taking input from user
    if cmd == "hold":
        gripper.hold()
        sleep(0.1)
        print(gripper.is_hold)


    if cmd == "drop":
        gripper.drop()
        sleep(0.1)
        print(gripper.is_hold)

    if cmd == "is_det":
        print(gripper.is_detected)
        
    if cmd == "is_hold":
        print(gripper.is_hold)

    if cmd == "stop":
        gripper.stop()
        break