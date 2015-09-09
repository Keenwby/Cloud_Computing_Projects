#!/usr/bin/python
#authour: Baiyang Wang
import os
import sys
import time
import boto.ec2.cloudwatch
#Read the total_time as users' need
total = raw_input("Please input the total time:")
total = (int)(raw_input("Please input the total time:"))
#cloudwatch
cw = boto.ec2.cloudwatch.connect_to_region('us-east-1', aws_access_key_id='AKIAIPJHPPGSZDOOZKKA', aws_secret_access_key='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')
#Get the query
q = os.popen("/usr/bin/mysql -u root -pdb15319root --execute=\"show status like \'Queries\'\"").read()
[n1, n2, q] = q.split('\t',2)
end_query = (int)(q)-3
print end_query
#Get the time
t = os.popen("/usr/bin/mysql -u root -pdb15319root --execute=\"show status like \'Uptime\'\"").read()
[n1, n2, t] = t.split('\t',2)
end_time = (int)(t)
print end_time
#####
for i in range(1, (total/60)+1):
    time.sleep(60)
    begin_query = end_query + 6
    begin_time = end_time
    q = os.popen("/usr/bin/mysql -u root -pdb15319root --execute=\"show status like \'Queries\'\"").read()
    [n1, n2, q] = q.split('\t',2)
    end_query = (int)(q)-3
    print "Test\t%d:\t%d" % (i, end_query)
    t = os.popen("/usr/bin/mysql -u root -pdb15319root --execute=\"show status like \'Uptime\'\"").read()
    [n1, n2, t] = t.split('\t',2)
    end_time = (int)(t)
    print "Test\t%d:\t%d" % (i, end_time)
    query_ratio = float((end_query - begin_query)/(end_time - begin_time)/128.1436812/16)
    print "Test\t%d:\t%f" % (i, query_ratio)
    cw.put_metric_data(namespace="baiyangw/TPS", name="TPS", unit="Percent", value=query_ratio)
