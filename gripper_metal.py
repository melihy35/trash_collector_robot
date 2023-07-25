from gripper_serial import GripperSerial
from threading import Thread
from time import sleep, time


class Gripper (Thread):
    MSG_HOLD = 'HOLD'
    MSG_DROP = 'DROP'
    MSG_FDB_IS_DET = 'IS_DET'
    MSG_FDB_IS_HOLD = 'IS_HOLD'
    DET_OK = 'DET_OK'
    DET_NOT_OK = 'DET_NOT_OK'
    HOLD_OK = 'HOLD_OK'
    HOLD_NOT_OK = 'HOLD_NOT_OK'
    MSG_FDB_IS_METAL = 'IS_METAL'

    def __init__(self, port="/dev/ttyACM0", baudrate=9600):
        Thread.__init__(self)
        self.serial = GripperSerial(port=port, baudrate=baudrate)

        self.is_hold = self.HOLD_NOT_OK
        self.is_detected = self.DET_NOT_OK

        self.is_mat_metal =False

        self.msg = self.MSG_DROP
        self.send = True

        self.stopped = False

    def run(self):
        start = time()
        while self.stopped is False:
            if time() - start > 0.1:
                self.is_detected = self.serial.write_and_read(self.MSG_FDB_IS_DET)
                self.is_hold = self.serial.write_and_read(self.MSG_FDB_IS_HOLD)
                start = time()

            if self.send:
                print(self.msg)
                if self.msg==self.MSG_FDB_IS_METAL:
                    met_s=self.serial.write_and_read_mat(self.msg)
                    #print("bu mat cins",met_s)
                    if met_s=='METAL':
                        self.is_mat_metal=True
                else:
                    msg = self.serial.write_and_read(self.msg)
                    self.is_mat_metal=False
                
                # msg = self.serial.write_and_read(self.msg)
                # self.is_mat_metal=False
                
                if msg == self.HOLD_OK:
                    self.is_hold = self.HOLD_OK
                elif msg == self.HOLD_NOT_OK:
                    self.is_hold = self.HOLD_NOT_OK

                self.send = False

    def stop(self):
        self.stopped = True
        self.join()

    def hold(self):
        self.msg = self.MSG_HOLD
        self.send = True
        sleep(0.1)


    def drop(self):
        self.msg = self.MSG_DROP
        self.send = True
        sleep(0.1)

    def material(self):
        # self.serial.write_and_read_mat(self.MSG_FDB_IS_METAL)
        self.msg = self.MSG_FDB_IS_METAL
        self.send = True
        sleep(0.1)
