#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	help.py
"""

import re
from yapsy.IPlugin import IPlugin

class help(IPlugin):

	def __init__(self):

		self.name="help"
		self.type="both"
		self.regexp=["^[hH]elp(me)?|^[Ii] need help"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="help"
		self.description="show help."
		self.answers="both"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):

		config=data['bot'].config

		output ="Avaliable commands are:";

		cmds=[]

		for plugin in data['bot'].plugins.getAllPlugins():

			validType=False
			validOrigin=False

			if data['msg_type'] in 'chat,normal':

				if plugin.plugin_object.type in "chat,normal,both":

					validType=True

			else:

				if plugin.plugin_object.type in "groupchat,both":

					validType=True

			if validType:

				if data['origin'] == 'xmpp':

					if plugin.plugin_object.answers in "xmpp,both":

						validOrigin=True
	
			if validOrigin and validType:

					cmds.append(plugin.plugin_object.syntax)

		if data['msg_type']=='chat':

			for cmd in sorted(cmds):

				output+="\n%s" % cmd
		else:

			for cmd in sorted(cmds):

				output+="\n%s %s" % (config.botname,cmd)

		data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
		
		return True

