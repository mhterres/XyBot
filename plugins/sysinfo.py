#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	sysinfo.py
"""

import re
import os
import sys

sys.path.insert(1,'%s/../' % os.path.dirname(os.path.realpath(__file__)))

from yapsy.IPlugin import IPlugin
from libs.ami import AMI
from libs.ami import AMIDict

from libs.asterisk_rt import getAsteriskRealtimeInformation

class sysInfo(IPlugin):

	def __init__(self):

		self.name="sysinfo"
		self.type="both"
		self.regexp=["^[sS]ysinfo"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="sysinfo"
		self.description="show Asterisk system informatio (admins only)"
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

					ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

					if not ami.connected:

						output="ERROR: It's not possible to connect to Asterisk."
						data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

						return False
					else:

						action = []
						action.append(('Action','CoreSettings'))
	
						ami.sendAction(action)
							
						try:

							AsteriskVersion=ami.lastDictAMI['AsteriskVersion']
						except:

							output="ERROR: It's not possible to get system information."

							data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

							return False
						else:

							action = []
							action.append(('Action','CoreStatus'))
			
							ami.sendAction(action)
							
							try:

								CoreStartupDate=ami.lastDictAMI['CoreStartupDate']
								CoreStartupTime=ami.lastDictAMI['CoreStartupTime']
								CoreReloadDate=ami.lastDictAMI['CoreReloadDate']
								CoreReloadTime=ami.lastDictAMI['CoreReloadTime']
								CoreCurrentCalls=ami.lastDictAMI['CoreCurrentCalls']
							except:

								output="ERROR: It's not possible to get system information."

								data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

								return False
							else:

								output ='Asterisk Version %s\n' % AsteriskVersion
								output+='Startup Time: %s %s\n' % (CoreStartupDate,CoreStartupTime)
								output+='Last Reload Time: %s %s\n' % (CoreReloadDate,CoreReloadTime)
								output+='Concurrent Active Calls: %s' % CoreCurrentCalls

								data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

								return True

		return False
		
