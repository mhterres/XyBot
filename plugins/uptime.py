#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	uptime.py
"""

import re
import time
import datetime
from yapsy.IPlugin import IPlugin

class uptime(IPlugin):

	def __init__(self):

		self.name="uptime"
		self.type="both"
		self.regexp=["^[uU]ptime$"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="uptime"
		self.description="show bot uptime."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		config=data['bot'].config

		now=str(time.time())

		output ="%s started at %s.\n" % (config.botname,(datetime.datetime.fromtimestamp(int(data['bot'].started.split(".")[0])).strftime('%Y-%m-%d %H:%M')))

		uptime=int(now.split(".")[0])-int(data['bot'].started.split(".")[0])

		days=0
		hours=0
		minutes=0
		seconds=0

		if uptime >= (86400):

			days=int(uptime/86400)
			uptime = uptime - (days*86400)

		if uptime >= 3600:

			hours=int(uptime/3600)
			uptime = uptime - (hours*3600)

		if uptime >= 60:

			minutes=int(uptime/60)
			uptime = uptime - (minutes*60)

		if uptime > 0:

			seconds=uptime

		strUptime=""

		if days > 0:

			strUptime += "%i day(s) " % days

		if hours > 0:

			strUptime += "%i hour(s) " % hours

		if minutes > 0:

			strUptime += "%i minute(s) " % minutes

		if seconds > 0:

			strUptime += "%i second(s) " % seconds

		output+="Uptime: %s" % strUptime

		data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
		
		return True

