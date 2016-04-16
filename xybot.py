#!/usr/bin/env python
# -*- coding: utf-8 -*-

#	xybot.py
#	XMPP MUC Bot that interacts with Asterisk
#
#	Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
#	2016/04/15
#
#	Initially based on mucbot.py example from SleekXMPP by Nathanael C. Fritz
#

import re
import os
import sys
import time

import logging
import sleekxmpp

sys.path.insert(1,'%s' % os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1,'%s/libs/' % os.path.dirname(os.path.realpath(__file__)))

from libs.config import Config
from libs.dbpgsql import DBPgsql
from libs.monitor import Monitor

from yapsy.PluginManager import PluginManager

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
	reload(sys)
	sys.setdefaultencoding('utf8')
else:
	raw_input = input


class XyBot(sleekxmpp.ClientXMPP):

	def __init__(self, jid, password, room, nick, confsrv):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)

		self.register_plugin('xep_0045') # Multi-User Chat (MUC)
		self.register_plugin('xep_0249') # Direct MUC Invitations

		self.confsrv = confsrv
		self.room = "%s@%s" % (room,confsrv)
		self.nick = nick

		# The session_start event will be triggered when
		# the bot establishes its connection with the server
		# and the XML streams are ready for use. We want to
		# listen for this event so that we we can initialize
		# our roster.
		self.add_event_handler("session_start", self.start)

		# The message event is triggered whenever a message
		# stanza is received. Be aware that that includes
		# MUC messages and error messages.
		self.add_event_handler("message", self.message)

		# The groupchat_presence event is triggered whenever a
		# presence stanza is received from any chat room, including
		# any presences you send yourself. To limit event handling
		# to a single room, use the events muc::room@server::presence,
		# muc::room@server::got_online, or muc::room@server::got_offline.
		self.add_event_handler("muc::%s::got_online" % self.room,
							   self.muc_online)

		self.add_event_handler("muc::%s::got_offline" % self.room,
							   self.muc_offline)


	def start(self, event):
		"""
		Process the session_start event.

		Typical actions for the session_start event are
		requesting the roster and broadcasting an initial
		presence stanza.

		Arguments:
			event -- An empty dictionary. The session_start
					 event does not provide any additional
					 data.
		"""
		self.send_presence()
		self.get_roster()
		self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

	def message(self, msg):
		"""
		Process incoming message stanzas. Be aware that this also
		includes MUC messages and error messages. It is usually
		a good idea to check the messages's type before processing
		or sending replies.

		Arguments:
			msg -- The received message stanza. See the documentation
				   for stanza objects and the Message stanza to see
				   how it may be used.
		"""
		body=msg['body']

		self.dbpgsql.saveMessage(msg['from'].user,msg['from'].bare,msg['to'].bare,body)
		logging.debug("Msg %s - type %s - mucnick %s - my nick %s" % (body, msg['type'], msg['mucnick'], self.nick))

		if msg['type'] in ('chat', 'normal'):
			self.messageParse(msg,"xmpp")

		elif msg['type'] == 'groupchat':

			if msg['mucnick'] != self.nick.lower() and self.nick in msg['body'].lower():
				self.messageParse(msg,"xmpp")

		else:
			# Handle errors?
			pass

	def enterRoom(self, room_name):

		self.plugin['xep_0045'].joinMUC(room_name + '@' + self.confsrv, self.nick, wait=True)

	def messageParse(self, msg, origin):

		cfg = self.config

		logging.debug("Parsing message %s." % msg)

		if msg['type'] == 'groupchat':

			msg_from = msg['mucnick']
			reply_to = msg['from'].bare

			cmd = re.sub('%s:' % self.nick, '', msg['body'], flags=re.IGNORECASE)
			cmd = re.sub('%s' % self.nick, '', cmd, flags=re.IGNORECASE)
			cmd = cmd.strip()

		else:

			msg_from = msg['from'].user
			reply_to = msg['from']
			cmd = msg['body']

		validCmd  = False
		processCmd = False
		validOrigin = False
	
		for plugin in pluginManager.getAllPlugins():

			#logging.debug("Processing plugin %s." % plugin.plugin_object.name)

			if msg['type'] == 'groupchat':

				if plugin.plugin_object.type in "groupchat,both":

					processCmd = True
			else:

				if plugin.plugin_object.type in "chat,normal,both":

					processCmd = True

			if processCmd:
	
				if origin == "xmpp":

					if plugin.plugin_object.answers in "xmpp,both":

						validOrigin = True

	 		if processCmd and validOrigin:

				m = plugin.plugin_object.match(cmd)

				if m:
					
					logging.debug("Using plugin %s." % plugin.plugin_object.name)

					validCmd = True

					self.event('run_%s' % plugin.plugin_object.name, data = {
							'bot' : self,
							'cmd' : cmd,
							'origin' : origin,
							'msg_from' : msg_from,
							'msg_to' : reply_to,
							'msg_body' : msg['body'],
							'msg_type' : msg['type'],
							'match' : m })

					break
			
		if not validCmd:

			# default answer

			returnmsg='I did not understand %s, %s.' % (cmd,msg_from)

			if msg['type']=='chat':

				returnmsg+='You can type help to discover valid (and maybe new) commands.'
			else:

				returnmsg+='You can type %s help to discover valid (and maybe new) commands.' % cfg.botname

			self.send_message(mto = reply_to,
							  mbody = returnmsg,
							  mtype = msg['type'])

	def muc_online(self, presence):
		"""
		Process a presence stanza from a chat room. In this case,
		presences from users that have just come online are
		handled by sending a welcome message that includes
		the user's nickname and role in the room.

		Arguments:
			presence -- The received presence stanza. See the
						documentation for the Presence stanza
						to see how else it may be used.
		"""

		if presence['muc']['nick'] != self.nick:

			self.send_message(mto=presence['from'].bare,
							  mbody="Hello %s. If you need HELP, let me know (xybot help)." % presence['muc']['nick'],
							  mtype='groupchat')

			self.dbpgsql.enterRoom(presence['muc']['nick'],presence['muc']['jid'].bare)

	def muc_offline(self, presence):
		"""
		Process a presence stanza from a chat room. In this case,
		presences from users that have just come offline are
		handled by sending a bye message that includes
		the user's nickname and role in the room.

		Arguments:
			presence -- The received presence stanza. See the
						documentation for the Presence stanza
						to see how else it may be used.
		"""

		if presence['muc']['nick'] != self.nick:

			self.dbpgsql.leaveRoom(presence['muc']['nick'],presence['muc']['jid'].bare)


if __name__ == '__main__':

	print "XyBot started at %s" % time.strftime("%c")

	botconfig = Config()

	print "DBPgsql connection."

	dbpgsql = DBPgsql(botconfig)

	xmpp = XyBot(botconfig.jid, botconfig.jid_pwd, botconfig.roomname, botconfig.botname, botconfig.confsrv)
	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0199') # XMPP Ping

	# DEBUG
	if botconfig.debug=="1":

		logging.basicConfig(filename=botconfig.logfile,level=logging.DEBUG,
							format='%(levelname)-8s %(message)s')
	else:
		logging.basicConfig(filename=botconfig.logfile,level=logging.INFO,
							format='%(levelname)-8s %(message)s')

	logging.info("Starting %s..." % botconfig.botname)

	pathname = os.path.dirname(sys.argv[0])
	path=os.path.abspath(pathname)

	log = logging.getLogger('yapsy')

	print "Plugins loading."

	pluginManager = PluginManager()
	pluginManager.setPluginPlaces(["%s/plugins/" % path])
	pluginManager.collectPlugins()

	dictPlugin={}
	for plugin in pluginManager.getAllPlugins():

		dictPlugin[plugin.plugin_object.name]=pluginManager.getPluginByName(plugin.plugin_object.name)
		xmpp.add_event_handler("run_%s" % plugin.plugin_object.name,plugin.plugin_object.execute, threaded=True)

	xmpp.plugins=pluginManager
	xmpp.dbpgsql=dbpgsql

	xmpp.plugins_path="%s/plugins/" % path
	xmpp.monitor_path="%s/monitor/" % path
	xmpp.monitor_scripts_path="%s/monitor/scripts/" % path

	xmpp.config=botconfig

	monitor=Monitor(xmpp,1)
	xmpp.monitor=monitor

	xmpp.started=str(time.time())

	print "Monitor started"

	monitor.start()

	print "XMPP Server connection"
	print "XyBot is running..."

	# Connect to the XMPP server and start processing XMPP stanzas.
	if xmpp.connect():
		# If you do not have the dnspython library installed, you will need
		# to manually specify the name of the server if it does not match
		# the one in the JID. For example, to use Google Talk you would
		# need to use:
		#
		# if xmpp.connect(('talk.google.com', 5222)):
		#	...
		xmpp.process(block=True)
		print "XyBot running..."
		logging.debug("Done")
	else:
		logging.error("Unable to connect.")
