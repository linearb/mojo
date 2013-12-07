#!/usr/bin/python2.5

import time
import datetime

datafile="/home/mojotronadmin/mmdata/incoming.log"

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    f = open(datafile,'a')
    # should probably make only one call to time routines but I'm lazy
    now_string = str(datetime.datetime.utcnow()) + ' UTC'
    f.write(str(int(time.time())) + "|" + now_string + "|" + environ['QUERY_STRING'] + "\n")
    f.close
    return ['ACK at ' + now_string + "\n"]

if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(myapp)
