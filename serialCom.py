import serial
from serial.tools import list_ports
import time

def initConnection(portNo,baudRate):
    try:
        ser = serial.Serial(portNo,baudRate,timeout=0.1)
        print("Device Connected")
        return ser
    except:
        print("Not Conneted d")

def sendData(se,data,basamak):
    buf="$"
    for i in data:
        buf +=str(i).zfill(basamak)
        #print(buf)
    try:
        se.write(buf.encode())
        print(buf)
    except:
        print("gonderim basarisiz")

if __name__ == "__main__" :

    ports = list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"Port: {port} Desc: {desc} Hwid: {hwid}")


    ser= initConnection("/dev/ttyACM0",9600)
    print(ser)
    while True:
        num = input(" enter a number :")
        ser.write(bytes(num,'utf-8'))
        time.sleep(0.01)
        print(ser.readline())
    ser.close()
    
    

