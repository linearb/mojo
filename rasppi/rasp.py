#!/usr/bin/python

"""Sound an alarm if a raspberry pi hasn't been heard from lately

To set an alarm for pi named 'pi', create a file in mmdata/pulse.d named pi.alarm

"""

import os.path
import time

pulse="/home/mojotronadmin/mmdata/pulse.d/"
logfile="/home/mojotronadmin/mmdata/incoming.log"

maxinterval = 15*60 # how many seconds without contact before sounding first alarm

alarm_once = False  # if True then only sound alarm once, then disable it
snooze = True       # if True then delay before re-sounding alarm
snoozedelay = 120*60    # in seconds

should_sendsms = True           # send an sms on alarm
alarm_smsnumber = "NEEDED" 

should_sendemail = False        # send an email on alarm
alarm_emailaddress = "dan@nachbar.com"

from twilio.rest import TwilioRestClient
def sendsms(tonumber, message):
    account_sid = "NEEDED"
    auth_token = "NEEDED"
    client = TwilioRestClient(account_sid, auth_token)
     
    twilio_number = "NEEDED"
    reply = client.messages.create(to=tonumber, from_=twilio_number, body=message)

import commands
def sendemail(toaddress, message):
    cmd = "echo '' | mail -s '{}' {}".format(message, toaddress)
    (status, output) = commands.getstatusoutput(cmd)
    # should catch error if status is not 0

def alarm(pi_name):
    message = pi_name + " is down."
    if should_sendsms:
        sendsms(alarm_smsnumber, message)
    if should_sendemail:
        sendemail(alarm_emailaddress, message)

# If alarm file '[piname].alarm' does not exist, the alarm for that pi is disabled.
# If that file is empty, the alarm goes off if maxdelay seconds have passed since last heard from pi.
# If it contains an integer the snooze is enabled. That sets the alarm to go off if maxdelay seconds 
# have passed since last alarm. If the alarm file contains anything else, the alarm is disabled.
def main():
    alarmfilelist = [x for x in os.listdir(pulse) if x.endswith(".alarm")]
    for filename in alarmfilelist:
        # get information about last time this pi contacted us
        last_timestamp = "0"
        pi_filename = filename[:-6]
        if os.path.exists(pulse + pi_filename):
            with open(pulse + pi_filename, 'r') as f:
                last_timestamp = f.readline().rstrip()          
            
        # if there is an alarm file, sound alarm if haven't heard from pi recently
        with open(pulse + filename, 'r+') as f:
            timestamp = f.readline().rstrip()
            if timestamp == "":
                timestamp = last_timestamp
            if timestamp.isdigit(): 
                now = time.time()
                if now - int(timestamp) > maxinterval:  
                    alarm(pi_filename)
                    if alarm_once:  
                        # only send alarm once, so disable alarm now
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
