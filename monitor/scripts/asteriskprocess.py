#!/usr/bin/python
# -*- coding: utf-8 -*-

# asteriskprocess.py
# return the status of asterisk process (running or not running)

import psutil

processFound=False

for proc in psutil.process_iter():

	try:
		pinfo = proc.as_dict(attrs=['pid', 'name'])
		if pinfo['name']=="asterisk":

			processFound=True

	except psutil.NoSuchProcess:
		pass

if processFound:

	returnmsg="running"
else:

	returnmsg="not running"
	
print returnmsg

