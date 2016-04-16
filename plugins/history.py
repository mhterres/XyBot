#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	history.py
"""

import re
from yapsy.IPlugin import IPlugin

class history(IPlugin):

	def __init__(self):

		self.name="history"
		self.type="groupchat"
		self.regexp=["^[hH]istory (.+)","^[hH]istory$"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="history [number of lines]"
		self.description="show conference room history."
		self.answers="both"

		self.default_lines=10

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):
		
		try:

			if data['match'].groups()[0].isdigit():

				lines = data['match'].groups()[0]
			else:

				lines = self.default_lines
		except:

			lines = self.default_lines

		data['bot'].send_message(mto=data['msg_to'],mbody=data['bot'].dbpgsql.listHistory(lines),mtype=data['msg_type'])
		return True

