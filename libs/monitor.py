#!/usr/bin/env python
# -*- coding: utf-8 -*-


#	monitor.py
#	Monitoring agent class
#
#	Marcelo Hartmann Terres <mhterres@gmail.com>
#	2016/04/15
#

import os
import sys
import glob
import time
import logging
import datetime
import ConfigParser

from threading import Thread
from subprocess import Popen, PIPE, STDOUT

class Monitor(Thread):

	def __init__(self,bot,num):

		Thread.__init__(self)
		self.num = num

		pathname = os.path.dirname(sys.argv[0])
		path=os.path.abspath(pathname)

		self.monitor_path="%s/monitor/" % path
		self.monitor_scripts_path="%s/monitor/scripts/" % path

		self.bot = bot

		files = glob.glob(self.monitor_path + "*.mon")

		monitors=[]

		for file in files:

			parser=ConfigParser.RawConfigParser()
			parser.read(file)

			monitors.append([parser.get("general","name"),parser.get("general","script"),parser.get("general","message"),parser.get("general","newmessage"),parser.get("general","check"),parser.get("general","integer"),parser.get("general","alwaysshowmessage"),"",""])

		self.monitors=monitors

		self.check(True,"","")

	def run(self):

		while True:

			logging.debug("Checking monitoring items every one minute...")

			self.check(False,"%s@%s" % (self.bot.config.roomname,self.bot.config.confsrv),"groupchat")
			time.sleep(60)

	def check(self,init,msg_to,msg_type):
		
		now = time.time()

		i = 0

		for monitor in self.monitors:

			check = False

			if not init:

				if now - int(monitor[7].split(".")[0]) > int(monitor[4]):

					check = True

			new = False

			if monitor[8] == "":

				new=True

			if init or check:

				cmd="%s/%s" % (self.monitor_scripts_path,monitor[1])

				p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
				output = p.stdout.read().replace("\r","").replace("\n","")

				logging.debug("Running %s - Output %s)" % (cmd,output))

				if not init:

					if not new:

						if monitor[6]=="1":

							if len(output)>0:

								self.msg(msg_to,monitor[3] % output,msg_type)
						else:

							if monitor[5]=="1":
					
								if output != monitor[8]:

									diff=int(output) - int(monitor[8])
									self.msg(msg_to,monitor[3] % str(diff),msg_type)
							else:

								if monitor[8] != output:
	
									self.msg(msg_to,monitor[3] % output,msg_type)

				self.monitors[i][7]=str(now)
				self.monitors[i][8]=output

			i=i+1

	def showMonitors(self,msg_to,msg_type):

		if len(self.monitors)==0:

			output="No monitoring agents available."
		else:

			output="Monitoring agents available:"

			for monitor in self.monitors:

				output+="\n%s - %s - %s" % (datetime.datetime.fromtimestamp(int(monitor[7].split(".")[0])).strftime('%Y-%m-%d %H:%M'),monitor[0],monitor[2] % monitor[8])

		self.msg(msg_to,output,msg_type)

	def msg(self,msg_to,msg,msg_type):

		self.bot.send_message(mto=msg_to,mbody=msg,mtype=msg_type)

		


