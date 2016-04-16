#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	update_monitoring.py
"""

import re
from yapsy.IPlugin import IPlugin

class uptime(IPlugin):

	def __init__(self):

		self.name="update monitoring"
		self.type="both"
		self.regexp=["^[uU]pdate monitoring$"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="update monitoring"
		self.description="make checks and update monitoring values."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		data['bot'].monitor.check(True,"","")

		output="All monitoring items checked."

		data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
		
		return True

