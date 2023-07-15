import serial

def initConnection(portNo, baudRate):
    try:
        ser = serial.Serial(portNo, baudRate)
        print("Cihaz Baðlandý")
        return ser
    except Exception as e:
        print("Baðlantý Kurulamadý:", str(e))
        return None

if __name__ == "__main__":
    ser = initConnection("/dev/ttyACM0", 9600)