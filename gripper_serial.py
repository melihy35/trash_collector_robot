import serial
from serial import Serial
from time import sleep


class GripperSerial:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = Serial()

        self.connect()

    def connect(self):
        if not self.serial.is_open:
            self.serial = Serial(self.port, self.baudrate, timeout=0.1)
            print("Serial connection at ", self.port)

    def disconnect(self):
        if self.serial.is_open:
            self.serial.close()

    def write(self, msg: int):
        self.serial.write(bytes(msg, 'utf-8'))

    def read(self):
        msg = self.serial.readline().decode('utf-8').rstrip('\n').rstrip("\r")
        return msg

    def write_and_read(self, msg: int):
        self.write(msg)
        sleep(0.05)
        return self.read()

