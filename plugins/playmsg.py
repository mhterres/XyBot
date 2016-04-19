#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	playmsg.py
"""

import re
import os
import sys

sys.path.insert(1,'%s/../' % os.path.dirname(os.path.realpath(__file__)))

from yapsy.IPlugin import IPlugin
from libs.ami import AMI
from libs.ami import AMIDict

from libs.asterisk_rt import getAsteriskRealtimeInformation

class playMsg(IPlugin):

	def __init__(self):

		self.name="playmsg"
		self.type="both"
		self.regexp=["^[pP]laymsg (.+)"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="playmsg <on|off>"
		self.description="enable/disable playing a message when answering a call (admins only)"
		self.answers="xmpp"

	def match(self,cmd):

		for regexp in self.re:

			m = regexp.match(cmd)

			if m:

				return m

		return False

	def execute(self,data):
		
		cfg=data['bot'].config

		if data['msg_type']=='chat':

			msg_jid=data['msg_to'].bare.split("/")[0]
		else:

			msg_jid="%s@%s" % (data['msg_from'].split("/")[0],cfg.xmpp_domain)

		realtime_data=getAsteriskRealtimeInformation(cfg,msg_jid)

		if realtime_data[0]==1:

			output=realtime_data[1]
			data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
			return False

		else:

			extension_number=realtime_data[2]
			extension_jid=realtime_data[3]
			extension_callerid=realtime_data[4]
			extension_allow_admin_cmd=realtime_data[7]

			if extension_number=="" or extension_jid=="":

				output = "Your jid (%s) needs to be linked with an asterisk extension." % msg_jid
				data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
				return False
			else:

				if not extension_allow_admin_cmd:

					output = "Your extension (%s) can't send administrative commands." % msg_jid
					data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
					return False
				else:

					option = data['match'].groups()[0]

					if option not in "on,off":

						output = "Valid options are on or off."
						data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
						return False
					else:

						ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

						if not ami.connected:

							output="ERROR: It's not possible to connect to Asterisk."
							data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

							return False
						else:

							if option=="on":

								action = []
								action.append(('Action','DBPut'))
								action.append(('Family','asterisk'))
								action.append(('Key','playmsg'))
								action.append(('Val','1'))
							else:

								action = []
								action.append(('Action','DBDel'))
								action.append(('Family','asterisk'))
								action.append(('Key','playmsg'))
	
							ami.sendAction(action)
							
							response=""

							try:

								response=ami.lastDictAMI['Response']
							except:

								response=""

							if response != "Success":

								if option=="on":

									output="ERROR: It's not possible enable the audio message."
								else:

									output="ERROR: It's not possible disable the audio message."

								data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

								return False
							else:

								if option=="on":

									output="Audio message is enabled."
								else:
									output="Audio message is disabled."

								data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

								return True

		return False
		
