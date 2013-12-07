#!/usr/bin/python2.5

import time
import datetime
import re
import os.path

datafile="/home/mojotronadmin/mmdata/incoming.log"
pulse="/home/mojotronadmin/mmdata/pulse.d/"

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    # should probably make only one call to time routines but I'm lazy
    now_string = str(datetime.datetime.utcnow()) + ' UTC'
    now_timestamp = str(int(time.time()))
    query_string = environ['QUERY_STRING']
    f = open(datafile,'a')
    f.write(now_timestamp + "|" + now_string + "|" + query_string + "\n")
    f.close
    # if a file for this ip address is in pulse.d, put the timestamp in it
    match_pi=re.search("local_ip=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\&id=([a-zA-Z0-9_]+)", query_string)
    which_ip = match_pi.group(1)
    which_name = match_pi.group(2)
    if os.path.exists(pulse+which_ip):
	    f = open(pulse+which_ip, 'w') 
	    f.write(now_timestamp + "\n")
	    f.write(which_name + "\n")
	    f.close
    return ['ACK at ' + now_string + "\n"]

if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(myapp)
