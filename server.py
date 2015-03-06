from flask import Flask, request, json
app = Flask(__name__)

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
        return json.dumps(data['sensors'], indent=4)
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
    file=open('testData.json','r')
    data = json.load(file)
    file.close()
    app.run(host='0.0.0.0', port=6789, debug=True)	
 
