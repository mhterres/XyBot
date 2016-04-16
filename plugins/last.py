#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	history.py
"""

import re
from yapsy.IPlugin import IPlugin

class last(IPlugin):

	def __init__(self):

		self.name="last"
		self.type="groupchat"
		self.regexp=["^[lL]ast (.+)","^[lL]ast$"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="last [number]"
		self.description="show last logons/logoffs in conference room."
		self.answers="both"

		self.default_items=5

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		try:

			if data['match'].groups()[0].isdigit():

				items = data['match'].groups()[0]
			else:

				items = self.default_items
		except:

			items = self.default_items

		data['bot'].send_message(mto=data['msg_to'],mbody=data['bot'].dbpgsql.getUserInOutInfo(items),mtype=data['msg_type'])

		return True
