from flask import Flask, request, json
app = Flask(__name__)

@app.route("/")
def hello():
    """Brief introduction message"""
    return "Hello this is the API server of a smart thermostate!"

@app.route('/temp', methods=['GET','PUT','POST'])
def showTemp():
    """Offers the three available methods of the api for the temperature sensors
    GET - Lists all the sensors values
    POST - Adds a new temperature sensor
    PUT - Delete all sensors
    """
    global data
    if request.method == 'GET':
        return json.dumps(data['sensors'], indent=4)
    if request.method == 'PUT':
        data['sensors'].clear()
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "All sensors deleted successfully"
    if request.method == 'POST':
        id = len(data['sensors'])+1
        temp= {str(id) : {"value":"0"}}		
        data['sensors'].update(temp)
        file = open('temps.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "New temperature value created successfully"
    else:
        return "Not a valid method"

@app.route('/temp/<tempid>')
def getTemp(tempid):
    """Retunrs the temperature of the sensor specified by <tempid>"""
    global data
    temp1 = data[sensors][tempid]["value"]
    return temp1

@app.route('/thermo', methods=['GET','POST','DELETE'])
def showThermo():
    """Offers the three available methods of the api for the thermostates
    GET - Lists all thermostates
    POST - Adds a default thermostate with no sensors assigned and 21 degree
    DELETE - Delete all thermostates
    """
    global data
    if request.method == 'GET':
        return json.dumps(data['thermostates'], indent=4) 
    if request.method == 'POST':
        id = len(data['thermostates'])+1
        thermo= {str(id) : {'sensors':[], 'temperature':'21'}}		
        data['thermostates'].update(thermo)
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "New thermostate created successfully"
    if request.method == 'DELETE':
        data['thermostates'].clear()
        file = open('testData.json','w')
        json.dump(data,file,indent=4)
        file.close()
        return "All thermostates deleted successfully"
    else:
        return "Not a valid method"


if __name__ == "__main__":
    file=open('testData.json','r')
    data = json.load(file)
    file.close()
    app.run(host='0.0.0.0', port=6789, debug=True)	
 
