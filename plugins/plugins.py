#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	plugins.py
"""

import re
from yapsy.IPlugin import IPlugin

class plugins(IPlugin):

	def __init__(self):

		self.name="plugins"
		self.type="both"
		self.regexp=["^([sS]how |[lL]ist )?[pP]lugins"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="show plugins"
		self.description="show plugins available in bot."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		output ="Installed plugins:";

		plgs=[]

		for plugin in data['bot'].plugins.getAllPlugins():

			plgs.append("%s - %s" % (plugin.plugin_object.name,plugin.plugin_object.description))


		for plg in sorted(plgs):

			output+="\n%s" % plg

		data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
		return True

