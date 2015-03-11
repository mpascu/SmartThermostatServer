from flask import Flask, request, json
import threading
import time
import socket

app = Flask(__name__)

class sensorReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print ('SENSOR SERVER STARTED')
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 5001))
        server_socket.listen(5)

    def run(self):    
        global data
        (client_socket, address) = server_socket.accept()
        while 1:
            size = len(data['sensors'])
            if (size!=0):
                client_socket.send (str(size))
                values = client_socket.recv(512)
                print "RECEIVED:" , values
                parsedValues = json.loads(values)
                for x in range(size):
                    data['sensors'][x][str(x+1)]['value'] = parsedValues[x]

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

@app.route('/thermo/<thermid>')
def getThermostate(thermid):
    """Retunrs the temperatfsfsdfsdfdsfdsfsd specified by <tempid>"""
    global data
    id = int(thermid)
    return json.dumps(data['thermostats'][id].get(str(id+1)), indent=4)

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
        thermo= {str(id) : {"name":request.form['name'], 'sensors':[], 'temperature':'21'}}		
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


if __name__ == "__main__":
    global data
    file=open('testData.json','r')
    data = json.load(file)
    file.close()
    mySensorReader =  sensorReader()
    mySensorReader.start()
    app.run(host='0.0.0.0', port=6789, debug=False)	
    mySensorReader.join()
