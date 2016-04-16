#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	bot_changelog.py
"""

import os
import re
import sys
import codecs
from yapsy.IPlugin import IPlugin

class bot_changelog(IPlugin):

	def __init__(self):

		self.name="bot changelog"
		self.type="both"
		self.regexp=["^([bB]ot )?[cC]hangelog$"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="bot changelog"
		self.description="show bot changelog."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		config=data['bot'].config

		pathname = os.path.dirname(sys.argv[0])
		path=os.path.abspath(pathname)

		output = codecs.open('%s/CHANGELOG' % path, 'r', 'utf-8')

		data['bot'].send_message(mto=data['msg_to'],mbody=output.read(),mtype=data['msg_type'])

		output.close()
		return True

