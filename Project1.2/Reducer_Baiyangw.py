#!/usr/bin/env python
#Filename: Reducer_Baiyangw.py
import sys
current_title = None
title = None
current_count=[0]*32
sum_count = 0
for line in sys.stdin:
    line = line.strip()
    title, value = line.split('\t',1)
    count, date = value.split('-',1)
#Extract the date infomation
    day = date[6:8]
    try:
        count = int(count)
        day = int(day)
    except ValueError:
            continue
    if current_title == title:
        current_count[day] += count
#Here comes a new word
    else:
        if current_title:
#Calculate the total numbers of viewing
            sum_count = sum(current_count)
            if sum_count > 100000:
                print '%d\t%s\t' % (sum_count, current_title),
#Output the daily numbers of viewing seperately
                for day in range(1,32):
                    if day < 10:
                        print '%s' % ('2014070'+str(day)),':','%d\t' % (current_count[day]),
                    else:
                        print '%s' % ('201407'+str(day)),':','%d\t' % (current_count[day]),
                print '\n'#Add an empty line after each line for better readability
        current_title = title
        current_count=[0]*32
        current_count[day] = count
#Output the last word if needed
if current_title == title:
    sum_count = sum(current_count)
    if sum_count > 100000:
        print '%d\t%s\t' % (sum_count, current_title),
        for day in range(1,32):
            if day < 10:
                print '%s' % ('2014070'+str(day)),':','%d\t' % (current_count[day]),
            else:
                print '%s' % ('201407'+str(day)),':','%d\t' % (current_count[day]),
        print '\n'