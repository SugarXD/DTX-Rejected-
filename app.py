#Turbine Farm server application
#Use https://turbine-farm.run.aws-usw02-pr.ice.predix.io/api/turbines/:turbine_id/sensors/:sensor_id
import requests, json, emailalerts, atexit, logging
from flask import Flask, url_for, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

#Create the application instance
app = Flask(__name__)

#Need loggin for background scheduler
logging.basicConfig()

#Return index route
@app.route("/")
def index():
	return redirect(url_for('static', filename='index.html'))

#Return all turbine data as a json
@app.route("/getAllData")
def getCurrentData():
	#Create list
	data = list()
	for i in range(1, 4):
		data.append(getTurbineData(i))

	alerts = list()
	alerts.append({"alert":"This is an alert"})

	dict_data = {"turbines":data, "alerts":alerts}
	return json.dumps(dict_data)

#Return one turbine's data as a json
@app.route("/getTurbineData/<id>/")
def getTurbineDataString(id):
	return json.dumps(getTurbineData(id))

#Return one turbine's data
def getTurbineData(id):
	#Get data
	turbine_temp = requests.get("https://turbine-farm.run.aws-usw02-pr.ice.predix.io/api/turbines/" + str(id) + "/sensors/temperature")
	turbine_volt = requests.get("https://turbine-farm.run.aws-usw02-pr.ice.predix.io/api/turbines/" + str(id) + "/sensors/voltage")
	turbine_stat = requests.get("https://turbine-farm.run.aws-usw02-pr.ice.predix.io/api/turbines/" + str(id) + "/heartbeat")
	data = dict()

	#Populate Dictionary
	data["id"] = str(id)

	#Temp json is real
	if json.loads(turbine_temp.text) == None:
		data["timestamp"] = "null"
		data["temp"] = "null"
	else:
		data["timestamp"] = json.loads(turbine_temp.text)['timestamp']
		data["temp"] = json.loads(turbine_temp.text)['value']

	#Volt json is real
	if json.loads(turbine_volt.text) == None:
		data["voltage"] = "null"
	else:
		data["voltage"] = json.loads(turbine_volt.text)['value']

	#Status json is real
	if json.loads(turbine_stat.text) == None:
		data["status"] = "null"
	else:
		data["status"] = json.loads(turbine_stat.text)['status']

	#Add color
	if data["status"] == "ONLINE":
		data["color"] = "success"
	else:
		data["color"] = "danger"

	return data


#Scheduling background data monitor
def check_data():
    for i in range(1, 4):
    	data = getTurbineData(i)

    	if data['status'] == "OFFLINE":
    		emailalerts.send_email(4, data['id'], "jaredad7.jd@gmail.com")
    		print "Sent an alert!"
    	else:
    		print "Turbine " + str(data['id'] + " is ONLINE!")

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=check_data,
    trigger=IntervalTrigger(seconds=5),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())