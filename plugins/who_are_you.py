#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	who_are_you.py
"""

import re
from yapsy.IPlugin import IPlugin

class who_are_you(IPlugin):

	def __init__(self):

		self.name="who are you"
		self.type="both"
		self.regexp=["^[wW]ho (are|r) (you\u)?"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="who are you?"
		self.description="show bot informations."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		output  = "Hi.\n"
		output += "My name is XyBot and I'm the a python XMPP bot that interacts with Asterisk.\n"
		output += "I'm developed by Marcelo Hartmann Terres <mhterres@mundoopensource.com.br> from Mundo Open Source website - https://www.mundoopensource.com.br/ and you can find my project web page at https://github.com/mhterres/XyBot\n\n"
		output += "Feel free to contact me anytime you want."

		data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
		
		return True

