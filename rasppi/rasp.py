#!/usr/bin/python

"""Sound an alarm if a raspberry pi hasn't been heard from lately

To set an alarm for ip_address, create a file in mmdata/pulse.d named {ip_address}.alarm

"""

import os.path
import time

pulse="/home/mojotronadmin/mmdata/pulse.d/"
logfile="/home/mojotronadmin/mmdata/incoming.log"

maxinterval = 15*60	# how many seconds without contact before sounding first alarm

alarm_once = False	# if True then only sound alarm once, then disable it
snooze = True		# if True then delay before re-sounding alarm
snoozedelay = 120*60	# in seconds

should_sendsms = True			# send an sms on alarm
alarm_smsnumber = "+18572031608" 

should_sendemail = False		# send an email on alarm
alarm_emailaddress = "phawley@alum.mit.edu"

from twilio.rest import TwilioRestClient
def sendsms(tonumber, message):
#	print "sms to " + tonumber + ", message:" + message
	account_sid = "ACd0d1259ef85c56be62b193c176e753cb"
	auth_token = "0603adfe203aca45daeb959fcc404af8"
	client = TwilioRestClient(account_sid, auth_token)
	 
	twilio_number = "+16173790273"
	reply = client.messages.create(to=tonumber, from_=twilio_number, body=message)


import smtplib  
def sendemail(toaddress, message):
	# not implemented: need smtp server
	print "email to " + toaddress + ", message:" + message
#	fromaddr = 'mojotronadmin@mm.mojotron.com'  
#	username = 'username'  
#	password = 'password'  
#	server = smtplib.SMTP('smtp.gmail.com:587')  
#	server.starttls()  
#	server.login(username,password)  
#	server.sendmail(fromaddr, toaddress, message)  
#	server.quit()  

def alarm(filename, pi_name):
	message = pi_name + ":" + filename + " has crashed"
	if should_sendsms:
		sendsms(alarm_smsnumber, message)
	if should_sendemail:
		sendemail(alarm_emailaddress, message)

# If alarm file "ipaddress.name" does not exist, the alarm for that ipaddress is disabled.
# If that file is empty, the alarm goes off if maxdelay seconds have passed since last ping from pi.
# If it contains an integer the snooze is enabled; the alarm goes off if maxdelay seconds 
# have passed since last alarm. If the alarm file contains anything else, the alarm is disabled.
def main():
	alarmfilelist = [x for x in os.listdir(pulse) if x.endswith(".alarm")]
	for filename in alarmfilelist:
		# get information about last time this pi contacted us
		last_timestamp = "0"
		last_name = "unknown"
		pi_filename = filename[:-6]
		if os.path.exists(pulse + pi_filename):
			with open(pulse + pi_filename, 'r') as f:
				last_timestamp = f.readline().rstrip()			
				last_name = f.readline().rstrip()			
			
		with open(pulse + filename, 'r+') as f:
			timestamp = f.readline().rstrip()
			if timestamp == "":
				timestamp = last_timestamp
			if timestamp.isdigit(): 
				now = time.time()
				if now - int(timestamp) > maxinterval:	
					# sound the alarm
					# print "alarm: " + pi_filename + "," + last_name
					alarm(pi_filename, last_name)
					if alarm_once: 	
						# disable alarm
						f.seek(0)
						f.write("disabled\n")
						f.truncate()
					elif snooze:	
						# reset alarm time to snoozedelay seconds in future
						f.seek(0)
						f.write(str(int(now + snoozedelay)) + "\n")
						f.truncate()

if __name__ == "__main__":
   main()
