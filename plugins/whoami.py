#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	whoami.py
"""

import re
import os
import sys
from yapsy.IPlugin import IPlugin

sys.path.insert(1,'%s/../' % os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1,'%s/../libs' % os.path.dirname(os.path.realpath(__file__)))

from libs.asterisk_rt import getAsteriskRealtimeInformation

class whoami(IPlugin):

	def __init__(self):

		self.name="who am i"
		self.type="both"
		self.regexp=["^[wW]ho am [iI]?"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="who am i?"
		self.description="show who am I."
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
		else:

			extension_number=realtime_data[2]
			extension_jid=realtime_data[3]
			extension_callerid=realtime_data[4]

			if realtime_data[5]:
				extension_allow_sms="Yes"
			else:
				extension_allow_sms="No"

			if realtime_data[6]:
				extension_allow_call="Yes"
			else:
				extension_allow_call="No"


 			output ="My Jabber ID: %s.\n" % extension_jid
			output+="My extension: %s.\n" % extension_number
			output+="My CallerID: %s.\n" % extension_callerid
			output+="Am I allowed to call: %s.\n" % extension_allow_call
			output+="Am I allowed to send SMS: %s." % extension_allow_sms

		data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
		
		return True

