import smtplib

def send_email(flag, turbine_id, recipient):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("jareddummyacct@gmail.com", "dummy123")
	if flag == 1:
	    msg = "ALERT - VOLTAGE BASED ERROR ENCOUNTERED AT TURBINE: "+str(turbine_id)+"\n"
	elif flag == 2:
		msg = "ALERT - THE TURBINE:"+str(turbine_id)+"OPERATING IN AN ENVIROMENT RATED TOO COLD FOR CONTINOUS OPERATION!\n"
	elif flag == 3:
		msg = "ALERT - THE TURBINE:"+str(turbine_id)+"OPERATING IN AN ENVIROMENT RATED TOO HOT FOR CONTINOUS OPERATION!\n"
	elif flag == 4:
		msg = "ALERT - THE TURBINE:"+str(turbine_id)+"IS OFFLINE!\n"

	server.sendmail("jareddummyacct@gmail.com", recipient, msg)
	server.quit()