#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dbpgsql.py
# DB Postgres class for interacting with xybot database
# see db/dbpgsql.sql for db schema
#
# Marcelo Hartmann Terres <mhterres@gmail.com>
# 2016/04/15
#

import logging
import psycopg2
import psycopg2.extras

class DBPgsql:

	def __init__(self,botconfig):

		self.dsn = 'dbname=%s host=%s user=%s password=%s' % (botconfig.dbpgsql_database,botconfig.dbpgsql_host,botconfig.dbpgsql_user,botconfig.dbpgsql_pwd)

		self.conn = psycopg2.connect(self.dsn)
		self.config=botconfig

	def getUserInOutInfo(self,items):

		# get informations about users entering and leaving chat room

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			sql="SELECT nick,operation,date FROM users_logs ORDER BY date desc limit %s;" % items

			curs.execute(sql)
		except:

			logging.error("Error searching database - SQL %s" % sql)

			returnmsg ="Error searching database."
			conn.commit()

		else:

			if not curs.rowcount:
			
				returnmsg = "There is no enough information right now."
			else:

				returnmsg=""

				rec=curs.fetchone()

				while rec is not None:

					returnmsg += "\nUser " + rec['nick'] + " " + rec['operation'] + " at " + rec['date'].strftime("%d/%m/%Y %H:%M:%S")
					rec=curs.fetchone()

			curs.close()

		return returnmsg

	def saveMessage(self,nick,msg_from,msg_to,message):

		# save message in db

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			curs.execute("INSERT INTO muc_chat (nick, msg_from, msg_to, message) VALUES(%s, %s , %s, %s);", (nick,msg_from,msg_to,message))
		except:

			logging.error("Can't save message in DB: %s, from %s to %s" % (message,msg_from,msg_to))

			self.conn.rollback()
		else:

			self.conn.commit()

		curs.close()

	def enterRoom(self,nick,jid):

		# save user information in db - enter room

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			curs.execute("INSERT INTO users_logs (nick, jid, operation) VALUES(%s, %s, %s);", (nick,jid,'logged in'))
		except:

			logging.error("Can't save user %s %s login DB" % (nick,jid))

			self.conn.rollback()
		else:

			self.conn.commit()

		curs.close()

	def leaveRoom(self,nick,jid):

		# save user information in db - leave room

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			curs.execute("INSERT INTO users_logs (nick, jid, operation) VALUES(%s,%s, %s);", (nick,jid,'logged off'))

		except:

			logging.error("Can't save user %s %s logoff DB" % (nick,jid))

			self.conn.rollback()
		else:

			self.conn.commit()

		curs.close()

	def listHistory(self,lines):

		# list room history

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			sql="SELECT date,nick,message from muc_chat ORDER BY date DESC limit %s;" % lines
			curs.execute(sql)

		except:

			logging.error("Error searching database - SQL %s" % sql)

			returnmsg ="Error searching database."
			conn.commit()

		else:

			returnmsg=""

			rec=curs.fetchone()

			while rec is not None:

				returnmsg += "\n[" + rec['date'].strftime("%d/%m/%Y %H:%M:%S") + "] - " + rec['nick'] + ": " + rec['message']

				rec=curs.fetchone()

			curs.close()

		return returnmsg

