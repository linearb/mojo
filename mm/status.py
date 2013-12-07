#!/usr/bin/python

import time
import datetime
import subprocess
import os

page_top = """
<html>
<head>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js">
</script>
<script>
$(document).ready(function(){
    $(".late").css("color","red");
});
</script>
</head>
<body>
"""

datafile="/home/mojotronadmin/mmdata/incoming.log"

def delta_string(delta_secs):
  if (delta_secs > (48*3600)):
    return "%d days" % (delta_secs/(24*3600))
  elif (delta_secs > (3*3600)):
    return "%d hours" % (delta_secs/3600)
  elif (delta_secs > (2*3600)):
    return "over two hours"
  elif (delta_secs > 3600):
    return "over an hour"
  elif (delta_secs > 180):
    return "%d minutes" % (delta_secs/60)
  elif (delta_secs > 120):
    return "2 minutes"
  elif (delta_secs > 60):
    return "1 minute"
  elif (delta_secs > 1):
    return ("%d seconds" % delta_secs)
  elif (delta_secs == 1):
    return ("one second")
  elif (delta_secs == 0):
    return ("zero seconds")
  else:
    return "ERROR - delta less than zero" + str(delta_secs)

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    now_secs = int(time.time())
    os.environ["TZ"]="US/Eastern"
    utc_string = time.asctime(time.gmtime(now_secs)) + " UTC"
    est_string = time.asctime(time.localtime(now_secs)) + " Eastern"
    ret_array  = []
    ret_array.append("<pre>")
    ret_array.append("Current time is:")
    ret_array.append(utc_string)
    ret_array.append(est_string)

    ret_array.append("")
    ret_array.append("</pre>")
    ret_array.append('<table border="1" cellpadding="5">')

    ret_string = subprocess.Popen(['/home/mojotronadmin/mmdata/get_tail'], stdout=subprocess.PIPE).communicate()[0]

    lines = ret_string.split("\n")

    ONE_WEEK = 60*60*24*7
    cut_off = now_secs - ONE_WEEK
    most_recent = {}
    is_late = {}
    qstring = {}
    time_stamp = {}
    time_string = {}
    delta_strings = {}
    local_ip = {}
    temperature = {}
    max_id_length = 0
    max_delta_length = 0
    max_time_length = 3
    for line in lines:
      if line.find("id=") > -1:
        # find the id, skip if zero length
        parts = line.partition("id=")
        id_parts = parts[2].partition("&")
        id = id_parts[0]
        if len(id) < 1:
          continue

        #ret_array.append("trying " + line)
        # make sure this isn't one we've seen before
        if id in most_recent:
          continue

        most_recent[id] = line
        if len(id) > max_id_length:
          max_id_length = len(id)
        parts = most_recent[id].split("|")
        if len(parts) != 3:
          ret_array.append("for key " + k + " didn't find three parts")
          qstring[id] = ""
          time_stamp[id] = ""
          continue

        time_stamp[id] = parts[0]
        time_string[id] = parts[1]
        qstring[id] = parts[2]

        if (now_secs - int(time_stamp[id])) > 60*10:
          is_late[id] = True
        else:
          is_late[id] = False

        delta_strings[id] = delta_string(now_secs - int(time_stamp[id]))
        if max_delta_length < len(delta_strings[id]):
          max_delta_length = len(delta_strings[id])

        qparts = qstring[id].split("&")
        q_dict = {}
        for qpart in qparts:
          one_part = qpart.partition("=")
          if len(one_part) < 3:
            ret_array.append("for key " + k + " didn't find three parts of " + qstring[id])
            time_stamp[id] = ""
            continue
          q_dict[one_part[0]] = one_part[2]

        for qk in q_dict.keys():
          if qk == "local_ip":
            local_ip[id] = q_dict[qk]
          elif qk == "temperature":
            temperature[id] = q_dict[qk]

    if len(ret_array) < 1:
      return ["ERROR - didn't find appropriate log entry - Complain to Dan.\n"]

    for k in sorted(most_recent.keys()):
      k_string = "%-0*s " % (max_id_length,k)
     # if k in time_stamp:
     #   ret_string += "%*s " % (max_time_length,time_stamp[k])
     # else:
     #   ret_string += " NO TIMESTAMP "

      if k in local_ip:
        local_ip_string = "%*s " % (-15,local_ip[k])
      else:
        local_ip_string = " NO LOCAL_IP "

      if k in temperature:
        t_temp = temperature[k] + " F"
      else:
        t_temp = ""
      t_string = "%*s" % (5,t_temp)

      if k in delta_strings:
        d_string = "%*s " % (max_delta_length,delta_strings[k])
      else:
        d_string = " NO TIME DELTA "

      #ret_array.append(k_string + d_string + "ago " + local_ip_string + t_string + most_recent[k])
      line_arr = []
      if is_late[k]:
        class_string = "late"
      else:
        class_string = "not_late"

      line_arr.append('<tr id="' + k_string + '" class="' + class_string + '">')
      for l in ( k_string, (d_string + "ago "), time_string[k], local_ip_string, t_string):
        line_arr.append('<td>' + l + '</td>')
      line_arr.append('</tr>')
      ret_array.append("".join(line_arr))

    ret_array.append("</body></html>")
    return [page_top + ("\n".join(ret_array))]


if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(myapp)
