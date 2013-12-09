#!/usr/bin/python

import rasp

def sendsms(tonumber, message):
    print "test: sending sms to " + tonumber + ": " + message


def sendemail(toaddress, message):
    print "test: email to " + toaddress + ", message:" + message

# redefine some constants and functions from rasp.py for testing
rasp.datafile = '../mmdata/incoming.log'
rasp.pulse = '../mmdata/pulse.d/'
rasp.should_sendemail = True
rasp.should_sendsms = True
rasp.sendsms = sendsms
#rasp.sendemail = sendemail
rasp.alarm_emailaddress = "patrick"

rasp.main()

