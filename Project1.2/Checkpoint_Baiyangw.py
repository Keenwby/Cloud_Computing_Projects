#!/usr/bin/env python
# Filename: Checkpoint_Baiyangw.py
import sys
from operator import itemgetter, attrgetter
List = []#Store all lines
d = [0]*32#Store the daily_view numbers of each lines
date = [0]*32#Store the date of each lines
Five = []#Store 5 target lines of Q10~11
Google = [0]*32#Store the line of 'Google' for Q12
Amazon = [0]*32#Store the line of 'Amazon' for Q12
line_num = 0
def assign():#Assign each daily-view numbers to target lines of Q10~Q13
    [d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[12],d[13],d[14],d[15],d[16],d[17],d[18],d[19],d[20],d[21],d[22],d[23],d[24],d[25],d[26],d[27],d[28],d[29],d[30],d[31]] = view.split('\t',30)
    for i in range (1,32):
        [date[i], d[i]] = d[i].split(':', 1)
        try:
            d[i] = int(d[i])
        except ValueError:
            continue
#Using sys input(command_line 'cat all files | ./Checkpoint_Baiyangw.py')
for line in sys.stdin:
    line = line.strip()
    if not len(line):#Skip empty lines
        continue
    [total_view, page_title, view] = line.split("\t", 2)
    List.append((int(total_view), page_title))
    if (page_title == 'Cristiano_Ronaldo') or (page_title == 'Neymar') or (page_title == 'Arjen_Robben') or (page_title == 'Tim_Howard') or (page_title == 'Miroslav_Klose') :
        assign()
        daily_max = max(d)
        Five.append((int(total_view), page_title, daily_max))
    if (page_title == 'Google') :
        assign()
        for i in range (1,32):
            Google[i] = d[i]
    if (page_title == 'Amazon.com') :
        assign()
        for i in range (1,32):
            Amazon[i] = d[i]
    if page_title == 'Dawn_of_the_Planet_of_the_Apes' :
        assign()
        Down_date = date[d.index(max(d))]
    line_num += 1
#Answer of Q7
print 'Q7: Total numbers of line is: ', line_num, '\n'
#Answer of Q8 & Q9
print 'Q8 & Q9: The most popular line is: ', max(List), '\nQ10:'
#Answer of Q10
Five_sorted_sum = sorted(Five, key=itemgetter(0), reverse=True)
for elem in Five_sorted_sum:
    print '%s\t%s' % (elem[0],elem[1])
print'\nQ11:'
#Answer of Q11
Five_sorted_daily = sorted(Five, key=itemgetter(2), reverse=True)
for elem in Five_sorted_daily:
    print 'Max_daily_view: ','%s' % (elem[2]), '\t%s' % (elem[1])
print'\nQ12:'
#Answer of Q12
count = 0
for i in range(1,32):
    if Google[i] > Amazon[i]:
        count += 1
print 'Google is more popular than Amazon in ', count, 'days\n'
#Answer of Q13
print 'Q13: The max-viewing date of Dawn_of_the_Planet_of_the_Apes is: ', '%s\n' % (Down_date)