#!/usr/bin/python
# -*- coding: utf-8 -*-

# queuemonitorholdtime.py
# return error when holdtime of a queue is greater than X seconds
#
# syntax: queuemonitorholdtime.py <queue name> <max holdtime>

import os
import sys
import time

sys.path.insert(1,'%s/../../' % os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1,'%s/../../libs' % os.path.dirname(os.path.realpath(__file__)))

from libs.config import Config
from libs.ami import AMI

cfg=Config()

try:

	queue = sys.argv[1]
except:

	print "You need to inform name of the queue."
	sys.exit(1)

try:

	maxholdtime = sys.argv[2]
except:

	print "You need to inform max hold time."
	sys.exit(1)


ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

events=ami.sendAction([("Action","QueueStatus"),("Queue",queue)])

foundQueue=False

for event in events:

		try:

			if (event['Event']=="QueueParams" and event['Queue']==queue):

				try:

					holdtime=event['Holdtime']
					foundQueue=True
					break
				except:
					holdtime=0
		except:

			pass

if not foundQueue:

	returnmsg="ERROR: can't get queue %s informations." % queue
else:

	if maxholdtime>=holdtime:

		returnmsg="Hold time of queue %s is minor or equal than %s seconds." % (queue,maxholdtime)
	else:

		returnmsg="ERROR: hold time of queue %s is %s seconds or greater."  % (queue,maxholdtime)

print returnmsg.strip()

