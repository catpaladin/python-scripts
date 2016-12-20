#!/usr/bin/env python
# Script to find most hits by IP in a hour from an Apache log.
# This script is under the assumption that the log file contains a single day
# and that the Apache logfiles are rotated, daily.
import sys

def work_log(logfile):
    with open(logfile) as log:
        #need time filter to segment by hour
        lines = log.readlines()
        for x in range(0,23):
            #segment_logs to return log by time
            x_ht = []
            set_date = ''
            for line in lines:
                searched = is_hour(line, x)
                if searched:
                    x_ht.append(searched[0])
                    set_date = searched[1]
                else:
                    continue
            if x_ht:
                #most_occurring(log) #[0] for ip, [1] for count
                ip_occ = most_occurring(x_ht)
                print set_date + " " + str(x) + ":00" + " - " + ip_occ[0] + ", " + str(ip_occ[1]) + " times"
            else:
                print "No hits for hour: " + str(x) + ":00"

def is_hour(line, hour):
    info = line.split(' ') #split the line by whitespace
    sel_hour = str(hour).zfill(2)
    parsed_date = info[3].split(':',1) #splits date in two
    date = parsed_date[0][1:] #get rid of that '[' by specifying [1:]
    parsed_time = parsed_date[1][0:2]
    if parsed_time == sel_hour:
        return line, date
    else:
        return

#search a log file for most occurring
def most_occurring(log_list):
    IP_ht = []
    hit_counter = {}
    for line in log_list:
        info = line.split(' ') #split the line by whitespace
        if info[0] in IP_ht:
            hit_counter[info[0]] += 1   #counter to find highest count
        else:
            hit_counter[info[0]] = 1
            IP_ht.append(info[0])  #build hashtable of IPs
    #sort through dictionary, reverse = True so that 0 provides highest count
    top = sorted(hit_counter, key=hit_counter.get, reverse=True)
    most = top[0]
    count = hit_counter[most]
    return most, count

if __name__ == "__main__":
    work_log(sys.argv[1])


# Sample output:
# >logcount.py apache.log
#10/01/2012 07:00 - 66.22.34.124, 5 hits
#10/01/2012 08:00 - 55.44.222.22, 10 hits
#10/01/2012 10:00 - 22.223.232.22, 1 hit
