import requests
import time
import threading
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from threading import Lock
from datetime import datetime

counter=0


class DataWrapper:
    def __init__(self, initial_value):
        self.value = initial_value

    def get_value(self):    #kendi değerimiz
        print(f"Kendi değerimiz ={self.value}")
        print(f"Dönen değer{self.value['value']}")
        return self.value['value']

    def get_seqN(self):
        #print(self.value)
        return self.value['seqNumber']

    def update_data(self, new_value):
        self.value = new_value 
        return self.value
# Custom JSON Encoder
class DataWrapperEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DataWrapper):
            # Convert the DataWrapper object to a JSON-serializable dictionary
            return o.value
        return super().default(o)
class myServer:
    def __init__(self,data,state):
        print("Server init")
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'ELE495'
        self.socketio = SocketIO(self.app, cors_allowed_origins='*')
        self.thread = None
        self.thread_lock = Lock()
        self.data = DataWrapper(data)  # Use the DataWrapper to store the data
        self.state = DataWrapper(state)

    def get_current_datetime(self):
        print("get time")
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def background_thread(self):
        print("background thread")
        print(f"ilk datamız:{self.data.value}")
        global counter

        while True:
            if self.data.get_value() == 'metal' and counter == self.data.get_seqN():
                self.socketio.emit('updateSensorData', {'date': self.get_current_datetime(), 'value': "metal",
                                                        'seqNumber': self.data.get_seqN()})
                self.socketio.emit('updateStateData',{'state' : "Aranıyor"})
                time.sleep(1)
                counter += 1
            elif self.data.get_value() == 'plastik' and counter == self.data.get_seqN():
                self.socketio.emit('updateSensorData', {'date': self.get_current_datetime(), 'value': "plastik" ,'seqNumber': self.data.get_seqN()})
                self.socketio.emit('updateStateData',{'state' : "Aranıyor"})
                time.sleep(1)
                counter += 1    
            else:  # data gelmiyorsa boş geçicek.
                #print("Cihaz daha bir değer almadi")
                time.sleep(1)

    def index(self):
        print("index")
        if request.method == 'POST':
            data = request.json
            print("Veri alındı:", data)
            if len(data)>2: # 2 den daha büyükse demekki normal datamız
                self.data.update_data(data)
                return jsonify(json.dumps(self.data,cls=DataWrapperEncoder))   
            else:
                self.state.update_data(data)
                print(f"Updated data:{data}")
                return jsonify(json.dumps(self.state,cls=DataWrapperEncoder))
            #self.socketio.emit('updateSensorData', {'value': self.data.get_value()})
            #return jsonify(json.dumps(self.data,cls=DataWrapperEncoder))
        else:
            return render_template('index.html', data=self.data.value)

    def connect(self):
        print('Client connected')
        with self.thread_lock:
            if self.thread is None:
                self.thread = self.socketio.start_background_task(self.background_thread)

    def disconnect(self):
        print('Client disconnected', request.sid)

    def run(self):
        print("run")
        self.app.route('/', methods=['GET', 'POST'])(self.index)
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('disconnect', self.disconnect)
        self.socketio.run(self.app, host='0.0.0.0', port=5000)
"""
def send_updated_data(url, new_data):
    # Send a POST request to update the data
    response = requests.post(url, json=new_data)

    # Check the response
    if response.status_code == 200:
        updated_data = response.json()
        print("Updated data:", updated_data)
    else:
        print("Failed to update data.")
"""
if __name__ == "__main__":
    data = {'value': "metal", 'seqNumber': 0}
    state = {'state' : None}
    dw = DataWrapper(data)
    st = DataWrapper(state)
    server = myServer(data,state)
    server.run()
