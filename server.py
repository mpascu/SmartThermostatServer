from flask import Flask, request, json
import RPi.GPIO as GPIO 
import threading
import time
import socket
import ast
import Adafruit_DHT

GPIO.setmode(GPIO.BCM) 
GPIO.setup(4, GPIO.OUT)  
GPIO.setup(17, GPIO.OUT)  
GPIO.setup(27, GPIO.OUT) 

USE_TEST_TEMPERATURES = False
app = Flask(__name__)

class sensorReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exitapp = False
        print ('SENSOR SERVER STARTED')
        if USE_TEST_TEMPERATURES:
            global server_socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('localhost', 5001))
            server_socket.listen(5)

    def run(self):    
        global data
        if USE_TEST_TEMPERATURES:
            (client_socket, address) = server_socket.accept()
            while not self.exitapp:
                size = len(data['sensors'])
                if (size!=0):
                    client_socket.send (str(size))
                    values = client_socket.recv(512)
                    #print "RECEIVED:" , values
                    parsedValues = json.loads(values)
                    for x in range(size):
                        data['sensors'][x][str(x+1)]['value'] = parsedValues[x]
        else:
            while not self.exitapp:
                humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 7)
                data['sensors'][0]['1']['value'] = str(int(temperature))
                print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
                time.sleep(1)

class actuatorTrigger(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exitapp = False

    def run(self):    
        global data
        pin = [4,17,27]
        while not self.exitapp:
            x=1
            tempCount = 0
            for t in data['thermostats']:
                mode=t.get(str(x))['mode']		
                if mode == 'ON':
                    GPIO.output(pin[x-1], True)
                if mode == 'OFF':    
                    GPIO.output(pin[x-1], False) 
                if mode == 'AUTO':
                    for s in t.get(str(x))['sensors']:
                        tempCount += int(data['sensors'][s-1][str(s)]['value'])    
                    '''print tempCount'''
                    avg = tempCount / float(len(t.get(str(x))['sensors']))
                    '''print avg'''
                    '''print t.get(str(x))['temperature']'''
                    if (float(t.get(str(x))['temperature'])-avg)<0.5:
                        GPIO.output(pin[x-1], True)
                    else:
                        GPIO.output(pin[x-1], False) 
                x=x+1
            time.sleep(1) 

@app.route("/")
def hello():
    """Brief introduction message"""
    return "Hello this is the API server of a smart thermostate!"

@app.route('/temp', methods=['GET','DELETE','POST'])
def showTemp():
    """Offers the three available methods of the api for the temperature sensors
    GET - Lists all the sensors values
    POST - Adds a new temperature sensor
    DELETE - Delete all sensors
    """
    global data
    if request.method == 'GET':
        return json.dumps(data.get('sensors'), indent=4)
    if request.method == 'DELETE':
        data['sensors'] = []
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "All sensors deleted successfully"
    if request.method == 'POST':
        id = len(data['sensors'])+1
        temp= {str(id) : {"value":"0", "name":request.form['name']}}		
        data['sensors'].append(temp)
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "New temperature value created successfully"
    else:
        return "Not a valid method"

@app.route('/thermo/<thermid>', methods=['GET','PUT'])
def getThermostate(thermid):
    """Retunrs the thermostat data specified by <thermid>"""
    global data
    id = int(thermid)
    if request.method == 'GET':
        return json.dumps(data['thermostats'][id-1].get(str(id)), indent=4)
    if request.method == 'PUT':
        temp = request.form['temperature']
        data['thermostats'][id-1].get(str(id))['temperature']=temp		
        mode = request.form['mode']
        data['thermostats'][id-1].get(str(id))['mode']=mode
        sensors = request.form['sensors']
        sensors= ast.literal_eval(sensors)
        data['thermostats'][id-1].get(str(id))['sensors']=sensors
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return ' ' 
@app.route('/thermo', methods=['GET','POST','DELETE'])
def showThermo():
    """Offers the three available methods of the api for the thermostates
    GET - Lists all thermostates
    POST - Adds a default thermostate with no sensors assigned and 21 degree
    DELETE - Delete all thermostates
    """
    global data
    if request.method == 'GET':
        return json.dumps(data['thermostats'], indent=4) 
    if request.method == 'POST':
        id = len(data['thermostats'])+1
        thermo= {str(id) : {"name":request.form['name'], 'sensors':[], 'temperature':'21', 'mode':'OFF'}}		
        data['thermostats'].append(thermo)
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "New thermostate created successfully"
    if request.method == 'DELETE':
        data['thermostats']=[]
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "All thermostates deleted successfully"
    else:
        return "Not a valid method"

def main():
    global data
    file=open('testData.json','r')
    data = json.load(file)
    file.close()
    mySensorReader =  sensorReader()
    mySensorReader.start()
    myActuatorTrigger =  actuatorTrigger()
    myActuatorTrigger.start()
    app.run(host='0.0.0.0', port=6789,threaded=True, debug=False)	
    try:
        mySensorReader.join()
        myActuatorTrigger.join()
    except KeyboardInterrupt:
        mySensorReader.exitapp = True
        myActuatorTrigger.exitapp = True
        GPIO.cleanup()

if __name__ == "__main__":
    main()
