from gripper_serial import GripperSerial


class Gripper:
    MSG_HOLD = '0'
    MSG_DROP = '1'
    MSG_FDB = '2'
    MSG_IR_OK = '3'
    MSG_IR_NOT_OK = '4'
    MSG_HOLD_OK = '5'
    MSG_HOLD_NOT_OK = '6'

    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.serial = GripperSerial(port=port, baudrate=baudrate)
        self.is_hold = False

    def state(self):
        return self.serial.write_and_read(self.MSG_FDB)

    def hold(self):
        state = self.serial.write_and_read(self.MSG_HOLD)
        if state == self.MSG_HOLD_NOT_OK:
            self.is_hold = False
            return False
        else:
            self.is_hold = True
            return True

    def drop(self):
        self.serial.write(self.MSG_DROP)

    def material(self):
        pass

