#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	enterqueue.py
"""

import re
import os
import sys

sys.path.insert(1,'%s/../' % os.path.dirname(os.path.realpath(__file__)))

from yapsy.IPlugin import IPlugin
from libs.ami import AMI
from libs.ami import AMIDict

from libs.asterisk_rt import getAsteriskRealtimeInformation

class enterQueue(IPlugin):

	def __init__(self):

		self.name="enterqueue"
		self.type="both"
		self.regexp=["^[eE]nter[qQ]ueue (.+)"]
		self.re = [ re.compile(expr) for expr in self.regexp ]
		self.syntax="enterqueue <queue name>"
		self.description="enter an extension in a queue"
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

			if extension_number=="" or extension_jid=="":

				output = "Your jid (%s) needs to be linked with an asterisk extension." % msg_jid
				data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])
				return False
			else:

					queue = data['match'].groups()[0]

					ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

					if not ami.connected:

						output="ERROR: It's not possible to connect to Asterisk."
						data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

						return False
					else:

						action = []
						action.append(('Action','QueueAdd'))
						action.append(('Queue',queue))
						action.append(('Interface',"%s/%s" % (cfg.siptype,extension_number)))
						action.append(('MemberName',extension_callerid))

						ami.sendAction(action)
						
						response=""

						try:

							response=ami.lastDictAMI['Response']
						except:

							response=""

						if response != 'Success':

							output="ERROR: It's not possible to enter %s on queue %s." % (extension_number,queue)
							data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

							return False
						else:

							output="Extension %s entered queue %s" % (extension_number,queue)
							data['bot'].send_message(mto=data['msg_to'],mbody=output,mtype=data['msg_type'])

							return True

		return False
		
