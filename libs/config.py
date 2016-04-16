#!/usr/bin/env python
# -*- coding: utf-8 -*-

# config.py
# configuration class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/04/15
#


import os
import sys
import ConfigParser

class Config:

	def __init__(self):

		configuration = ConfigParser.RawConfigParser()

		configuration = ConfigParser.RawConfigParser()
		configuration.read('/etc/xybot/xybot.conf')

		self.botname=configuration.get('general','botname')
		self.logfile=configuration.get('general','logfile')
		self.debug=configuration.get('general','debug')

		# xmpp
		self.jid=configuration.get('xmpp','jid')
		self.jid_pwd=configuration.get('xmpp','jid_pwd')
		self.xmpp_domain=configuration.get('xmpp','xmpp_domain')
		self.roomname=configuration.get('xmpp','roomname')
		self.confsrv=configuration.get('xmpp','confsrv')

		# dbpgsql
		self.dbpgsql_host=configuration.get('dbpgsql','dbpgsql_host')
		self.dbpgsql_database=configuration.get('dbpgsql','dbpgsql_database')
		self.dbpgsql_user=configuration.get('dbpgsql','dbpgsql_user')
		self.dbpgsql_pwd=configuration.get('dbpgsql','dbpgsql_pwd')

		# asterisk
		self.ami_srv=configuration.get('asterisk','ami_srv')
		self.ami_port=configuration.get('asterisk','ami_port')
		self.ami_user=configuration.get('asterisk','ami_user')
		self.ami_secret=configuration.get('asterisk','ami_secret')

		self.ast_db_host=configuration.get('asterisk','ast_db_host')
		self.ast_db_name=configuration.get('asterisk','ast_db_name')
		self.ast_db_user=configuration.get('asterisk','ast_db_user')
		self.ast_db_pwd=configuration.get('asterisk','ast_db_pwd')

		self.ast_sip_table=configuration.get('asterisk','ast_sip_table')
		self.ast_jid_field_prefix=configuration.get('asterisk','ast_jid_field_prefix')

