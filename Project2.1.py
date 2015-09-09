#!/usr/bin/env python
#Filename: project2.1_baiyangw.py
import boto.ec2
import urllib2
import time
import re
rule = re.compile(r'[1-9]\d*\.\d\d*')
#Create a connection
conn = boto.ec2.connect_to_region("us-east-1")
#Create a security group
web = conn.create_security_group('Project2.1', 'baiyangw')
web.authorize('tcp',80,80,'0.0.0.0/0')
#Launch the load generator
load_generator = conn.run_instances(
    'ami-1810b270',
    key_name='Baiyangw',
    instance_type='m3.medium',
    security_groups=['Project2.1'])
#tag
while True:
    try:
        if load_generator.instances[0].update()=='running':
            load_generator.instances[0].add_tag('Project','2.1')
            print 'lg tag added!'
            break
    except:
        continue
#Visit the Load Generator
while True:
    try:
        if load_generator.instances[0].public_dns_name != '':
            dns_lg = load_generator.instances[0].public_dns_name
            print 'dns_lg = ', dns_lg
            break
    except:
        continue
while True:
    try:
        get = urllib2.urlopen('http://' + dns_lg +'/username?username=baiyangw/')
        print 'lg_url got!'
        break
    except:
        continue
dc_num = 0
sumrps = 0.0
while True:
#Launch data center
    data_center = conn.run_instances(
        'ami-324ae85a',
        key_name='Baiyangw',
        instance_type='m3.medium',
        security_groups=['Project2.1'])
#Count data center numbers    
    dc_num += 1
#tag
    while True:
        try:
            if data_center.instances[0].update()=='running':
                data_center.instances[0].add_tag('Project','2.1')
                print 'dc tag added!'
                break
        except:
            continue
#Visit the Load Generator
    while True:
        try:
            if data_center.instances[0].public_dns_name != '':
                dns_dc = data_center.instances[0].public_dns_name
                print 'dns_dc = ', dns_dc
                break
        except:
            continue
    while True:
        try:
            get = urllib2.urlopen('http://' + dns_dc +'/username?username=baiyangw/')
            print 'url_dc got!'
            break
        except:
            continue
    time.sleep(30)
#Submit
    url = "http://" + dns_lg + "/part/one/i/want/more?dns=" + dns_dc + "&testId=Pizza"
    while True:
        try:
            get = urllib2.urlopen(url)
            break
        except:
            continue
#Visit the .txt url
    url = 'http://' + dns_lg + '/view-logs?name=result_baiyangw_Pizza.txt'
    while True:
        try:
            data = urllib2.urlopen(url).read()
            print data
            break
        except:
            continue
#Pick rps numbers
    num = rule.findall(data)
    for i in range(-dc_num,0):
        num[i] = float(num[i])
        print 'Instance number:' + dc_num + '\t' + 'rps:' + num[i] + '\n'
    sumrps = sum(num)
    print 'Sum = ' + sumrps
    if sumrps > 3600.00:
        break
    else:
        time.sleep(80)