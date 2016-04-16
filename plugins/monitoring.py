#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	monitoring.py
"""

import re
from yapsy.IPlugin import IPlugin

class monitoring(IPlugin):

	def __init__(self):

		self.name="monitoring"
		self.type="both"
		self.regexp=["^([sS]how )?[mM]onitoring (items)?"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="show monitoring items"
		self.description="show monitoring items."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		data['bot'].monitor.showMonitors(data['msg_to'],data['msg_type'])

		return True

