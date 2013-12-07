#!/usr/bin/python

import nmm

def my_print(a, b):
	print a, b

nmm.datafile = '../mmdata/incoming.log'
nmm.pulse = '../mmdata/pulse.d/'
print nmm.myapp({'QUERY_STRING':'action=report&local_ip=192.168.2.147&id=den_at_number_4'}, my_print)


