#!/usr/bin/python2.5

import time
import datetime
import re
import os.path

datafile="/home/mojotronadmin/mmdata/incoming.log"
pulse="/home/mojotronadmin/mmdata/pulse.d/"

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    now_string = str(datetime.datetime.utcnow()) + ' UTC'
    now_timestamp = str(int(time.time()))
    query_string = environ['QUERY_STRING']
    f = open(datafile,'a')
    f.write(now_timestamp + "|" + now_string + "|" + query_string + "\n")
    f.close
    # if a file with this pi's name is in pulse.d, put the timestamp in it
    match_pi=re.search("local_ip=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\&id=([a-zA-Z0-9_]+)", query_string)
    if match_pi:
        which_name = match_pi.group(2)
        if os.path.exists(pulse+which_name):
            f = open(pulse+which_name, 'w') 
            f.write(now_timestamp + "\n")
            f.close
    return ['ACK at ' + now_string + "\n"]

if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(myapp)
