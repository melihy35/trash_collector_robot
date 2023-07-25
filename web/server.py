import random
import requests
from flask import Flask, render_template, request ,jsonify
from flask_socketio import SocketIO, emit 
from threading import Lock
from datetime import datetime


class myServer:
    def __init__(self,data):    #data kullanýcýdan gelecek veri olarak düþündük.
        print("Server init")
        self.app= Flask(__name__)
        self.app.config['SECRET_KEY'] = 'ELE495'
        self.socketio = SocketIO(self.app,cors_allowed_origins='*')
        self.thread = None
        self.thread_lock = Lock()
        self.data=data
        self.gonder=None
    
    def get_current_datetime(self):
        print("get time")
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")
    
    def background_thread(self,data):
        print("background thread")
        global seqNumber
        prev_seqNumber = -1  # Önceki seqNumber'ý saklayalým
        print(self.data)

        while True:
            if self.data == 'metal':
                self.socketio.emit('updateSensorData', {'date': self.get_current_datetime(), 'value': "metal"})
                #prev_seqNumber = self.seqNumber  # Önceki seqNumber'ý güncelle
            elif self.data == 'plastik':
                self.socketio.emit('updateSensorData', {'date': self.get_current_datetime(), 'value': "metal"})
                #prev_seqNumber = self.seqNumber  # Önceki seqNumber'ý güncelle
            else:  # data gelmiyorsa boþ geçicek.
                print("Cihaz daha bir deðer almadi")
                #self.socketio.sleep(2)
    def index(self):
        print("index")
        return render_template('index.html')

    def veri_al(self,data): # veriyi burada iþleyip gönderelim
        data =request.json
        print("Veri alýndý")
        self.socketio.emit('updateSensorData',{'value': self.data})

    def veri_gonder(self,gonder):
        url='https://localhost:5000/'
        response = requests.post(url,json=self.gonder)
        


    def connect(self):
        print('Client connected')
        with self.thread_lock:
            if self.thread is None:
                self.thread = self.socketio.start_background_task(self.background_thread,self.data)

    def disconnect(self):
        print('Client disconnected', request.sid)

    def run(self):
        print("run")
        self.app.route('/',methods=['POST','GET'])(self.index,self.veri_al)
        self.socketio.on_event('connect',self.connect)
        self.socketio.on_event('disconnect',self.disconnect)
        self.socketio.run(self.app, host='0.0.0.0',port=5000)

if __name__ == "__main__":

    serv=myServer("ele")
    serv.veri_gonder("metal")