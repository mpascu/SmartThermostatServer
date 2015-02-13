from flask import Flask, request, json
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route('/temp', methods=['GET','PUT','POST'])
def showTemp():
	if request.method == 'GET':
		file = open('temps.json','r')
		return file.read()
		file.close()
	if request.method == 'PUT':
		file = open('temps.json','w')
		data = {
			'temperatures':[],
			'quantity':'0'
		}
		json.dump(data,file)
		file.close()
		return json.dumps(data, indent=2);
	if request.method == 'POST':
		file = open('temps.json','r')
		jsonData = json.load(file)
		file.close()
		id = int( jsonData["quantity"] )+1
		temp= [{"id":str(id) , "value":"0"}]		
		jsonData["temperatures"]=jsonData["temperatures"]+temp
		jsonData["quantity"]=id-1	
		file = open('temps.json','w')
		json.dump(jsonData,file)
		file.close()
		return "New temperature value created successfully"
	else:
		return "Not a valid method"

@app.route('/temp/<int:tempid>')
def getTemp(tempid):
	file=open('temps.json','r')
	data = json.load(file)
	file.close()
	temp1 = data["temperatures"][tempid]["value"]
	return temp1

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=6789, debug=True)
