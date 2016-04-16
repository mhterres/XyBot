#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	sms.py
"""

import re
import os
import sys

sys.path.insert(1,'%s/../' % os.path.dirname(os.path.realpath(__file__)))

from yapsy.IPlugin import IPlugin
from libs.ami import AMI
from libs.ami import AMIDict

from libs.asterisk_rt import getAsteriskRealtimeInformation

class call(IPlugin):

	def __init__(self):

		self.name="sms"
		self.type="both"
		self.regexp=["^[sS][mM][sS] (.+)"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="sms <number> <message>"
		self.description="send SMS. (UNDER DEVELOPMENT)"
		self.answers="xmpp"

		self.sms_context="sms"
		

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

		dataItems=data['match'].groups()[0].split()

		if len(dataItems)<2:

			output="You need to inform the message."
			data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
			return False
		else:

			itemNum=0
			message=""
			for item in dataItems:

				if itemNum>=1:

					message="%s %s" % (message,item)

				itemNum+=1

			message=message.strip()

		realtime_data=getAsteriskRealtimeInformation(cfg,msg_jid)

		if realtime_data[0]==1:

			output=realtime_data[1]
			data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
			return False
		else:

			extension_number=realtime_data[2]
			extension_jid=realtime_data[3]
			extension_callerid=realtime_data[4]
			extension_allow_sms=realtime_data[5]

			if extension_number=="" or extension_jid=="":

				output = "Your jid (%s) needs to be linked with an asterisk extension." % msg_jid
				data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
				return False
			else:

				if not extension_allow_sms:

					output = "Your extension (%s) can't send SMS using XMPP." % extension_number
					data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
					return False
				else:

					number = dataItems[0]

					ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

					if not ami.connected:

						output="ERROR: It's not possible to connect to Asterisk."
						data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

						return False
					else:

						# sendSMS Action
						# This action is not implemented because it depends of the GSM hardware used
						# That's the reason of the commented code below
						action = []
						#action.append(('key','value'))

						#ami.sendAction(action)
						
						#response=""

						#try:

							#response=ami.lastDictAMI['Response']
						#except:

							#response=""

						#if response != 'Success':

							#output="ERROR: It's not possible to send %s to %s." % (message,number)
							#data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

							#return False
						#else:

							#output="Dialing to %s" % number
							#data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

					  # This follow 2 lines are here just to return some information
						output="Sending message %s to %s.\nThis is not implemented because depends of the GSM hardware used." % (message,number)
						data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])


						return True

		return False
		
