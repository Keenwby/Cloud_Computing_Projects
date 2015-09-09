#!/usr/bin/env python
#Filename: project2.2.py
#author: baiyangw
#1.Create ELB
import time
import urllib2
import boto.ec2
import boto.ec2.elb
from boto.ec2.elb import HealthCheck
conn = boto.ec2.connect_to_region('us-east-1')
lb_conn = boto.ec2.elb.connect_to_region('us-east-1')
zones = ['us-east-1c']
ports= [(80, 80, 'http')]
lb = lb_conn.create_load_balancer('baiyangwlb', zones,ports)
hc = HealthCheck(
	    access_point = 'baiyangwlb',
            interval=30,
            healthy_threshold=3,
            unhealthy_threshold=5,
            target='HTTP:80/heartbeat?username=baiyangw')
lb.configure_health_check(hc)
elb_name = lb.dns_name
print '1.The elb_address is: ' + lb.dns_name
import boto.ec2.autoscale
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy
#2.Create LC
asg_conn = boto.ec2.autoscale.connect_to_region('us-east-1')
lc = LaunchConfiguration(name='baiyangwlc',
                         image_id='ami-ec14ba84',
                         key_name='Baiyangw',
                         instance_type='m3.medium',
                         instance_monitoring = True,
                         security_groups=['Project'])
asg_conn.create_launch_configuration(lc)
print '2.lc creation success!'
#3.Create ASG
asg = AutoScalingGroup(group_name='baiyangwgroup',
			  load_balancers=['baiyangwlb'],
			  health_check_type = 'ELB',
			  health_check_period = '300',
			  desired_capacity = 1,
			  availability_zones=['us-east-1c'],
			  launch_config = lc,
			  min_size = 1,
			  max_size = 2,
			  tags = [boto.ec2.autoscale.tag.Tag(key='Project',value='2.2', 
				  resource_id='baiyangwgroup', propagate_at_launch=True)])
asg_conn.create_auto_scaling_group(asg)
print '3.auto scaling group created!'
#4.Create SP
scale_up_policy = ScalingPolicy(
		  name = 'scale_up',
		  adjustment_type = 'ChangeInCapacity',
        	  as_name ='baiyangwgroup',
	          scaling_adjustment = 1,
		  cooldown = 60
		)
scale_down_policy = ScalingPolicy(
		  name = 'scale_down',
		  adjustment_type = 'ChangeInCapacity',
	 	  as_name = 'baiyangwgroup',
	          scaling_adjustment = -1,
	          cooldown = 60
		)
asg_conn.create_scaling_policy(scale_up_policy) 
asg_conn.create_scaling_policy(scale_down_policy)
print '4-1.set up scaling policy'
scale_up_policy = asg_conn.get_all_policies(
	        as_group = 'baiyangwgroup',
	        policy_names = ['scale_up'])[0]
scale_down_policy = asg_conn.get_all_policies(
		as_group = 'baiyangwgroup',
	        policy_names = ['scale_down'])[0]
print '4-2.scaling policy updated'
#5.Create CW
import boto.ec2.cloudwatch
from boto.ec2.cloudwatch import MetricAlarm
cloudwatch = boto.ec2.cloudwatch.connect_to_region('us-east-1')
arn_name = 'us-east-1:476947093812:baiyangw'
alarm_dimensions = {"AutoScalingGroupName": 'baiyangwgroup'}
scale_up_alarm = MetricAlarm(   # create an alarm for when to scale up
		 name='scale_up_on_cpu',
         namespace='AWS/EC2',
         metric='CPUUtilization',
         statistic='Average',
		 comparison='>',
		 threshold='85',
		 period='60',
         evaluation_periods=3,
		 alarm_actions=[scale_up_policy.policy_arn, arn_name],
         dimensions=alarm_dimensions
		)
cloudwatch.create_alarm(scale_up_alarm)
print '5-1.cloud watch up finished'
scale_down_alarm = MetricAlarm(
         name='scale_down_on_cpu',
         namespace='AWS/EC2',
		 metric='CPUUtilization',
         statistic='Average',
		 comparison='<',
		 threshold='55',	
		 period='60',
         evaluation_periods=2,
         alarm_actions=[scale_down_policy.policy_arn, arn_name],
         dimensions=alarm_dimensions
		)
cloudwatch.create_alarm(scale_down_alarm)	
print '5-2.cloud watch down finished'
#6.Create a load generator
load_generator = conn.run_instances(
    'ami-562d853e',
    key_name='Baiyangw',
    instance_type='t1.micro',
    security_groups=['Project'])
#tag
while True:
    try:
        if load_generator.instances[0].update()=='running':
            load_generator.instances[0].add_tag('Project','2.2')
            print '6-1.lg tag added!'
            break
    except:
        time.sleep(1)
        print 'Tag again!'
        continue
#activate
while True:
    try:
        if load_generator.instances[0].public_dns_name != '':
            dns_lg = load_generator.instances[0].public_dns_name
            print '6-2.dns_lg = ', dns_lg
            break
    except:
        time.sleep(1)
        print 'dnsget again!'
        continue
time.sleep(10)
while True:
    try:
        get = urllib2.urlopen('http://' + dns_lg +'/username?username=baiyangw')
        print '6-3.url_lg got!'
        break
    except:
        time.sleep(1)
        continue
print 'Start to sleep 200s and wait for warm up'
time.sleep(240)
print '240s has passed'
#7.Warm up
url_wr = 'http://' + dns_lg +'/warmup?dns='+ elb_name + '&testId=Baiyangw'
print url_wr
for i in range(1,4):
	print "Warm up" + i + 'start'
	while True:
    		try:
    			urllib2.urlopen(url_wr)
        		print '7-1. request suceed'
        		break
    		except:
			time.sleep(1)
			print 'Again!'
        		continue
	time.sleep(10)
	url_txt = 'http://' + dns_lg + '/view-logs?name=warmup_baiyangw.txt'
	print i + 'time visit' + url_txt
	while True:
    		while True:
    			try:
				get = urllib2.urlopen(url_txt).read()
				print 'Warmup.txt' + i + 'get!'
				break
        		except:
            			print 'Again!'
            			continue
    		try:
    			if get.find('completed')!=-1:
				print '7-2.  ' + i + 'warm up completed'
				break
    		except:
			time.sleep(30)
        		continue
time.sleep(10)
#8.Start test
url_st = 'http://' + dns_lg +'/begin-phase-2?dns='+ elb_name + '&testId=Baiyangw'
while True:
    try:
    	urllib2.urlopen(url_st)
	print '7-3.test started'
        break
    except:
    	print 'Again!'
        continue
url_final ='http://' + dns_lg + '/view-logs?name=result_baiyangw_Baiyangw.txt'
print url_final
#9.Sleep
time.sleep(6060)
#10.Shutdown
asg.shutdown_instances()
time.sleep(10)
asg.delete()
time.sleep(10)
lc.delete()
time.sleep(10)
