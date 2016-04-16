# -*- coding: utf-8 -*-

# ami.py
# Asterisk AMI Class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/04/15
#

import time
import socket

def recv_timeout(s,timeout=.5):
    #make socket non blocking
    s.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = s.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data)
 
class AMI:

	def __init__(self,ami_srv,ami_port,ami_user,ami_secret):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ami_srv,int(ami_port)))

		loginAction ="Action: Login\n"	
		loginAction+="Username: %s\n" % ami_user
		loginAction+="Secret: %s\n" % ami_secret
		loginAction+="Events: off\n"
		loginAction+="\n"
	
		s.send(loginAction)

		data=recv_timeout(s)
		amiDict=AMIDict(data)

		dictConnect=amiDict.getValue('Response')

		if dictConnect=="Success":

			#print "AMI Connected with success"
			self.connected=True

		else:
			#print "AMI Connected failed"
			self.connected=False
		
		self.socket = s

		self.lastEvents=amiDict.events
		self.lastDictAMI=amiDict.dictAMI

	def sendAction(self,actionData):

		action=""

		for data in actionData:

			action+="%s: %s\n" % (data[0],data[1])

		action+="\n"

		self.socket.send(action)

		data=recv_timeout(self.socket)
		amiDict=AMIDict(data)
		dictio=amiDict.events

		self.lastEvents=amiDict.events
		self.lastDictAMI=amiDict.dictAMI

		return dictio

class AMIDict:

	def __init__(self,data):

		events=[]
		dictAMI={}

		# split the data
		lines = data.split('\n')

		event=False

		for item in lines:

			item=item.replace("\r","")

			if len(item.strip())>0 and ":" in item:

				amiLine=item.split(":",1)

				try:

					title=amiLine[0].strip()
				except:

					title=""

				try:

					value=amiLine[1].strip()
				except:

					value=""

				if not event:

					if title=="Event":
	
						event=True
						newEvent=value
						newEventDict={}

						newEventDict.update({title:value})
				else:

						newEventDict.update({title:value})

				dictAMI.update({title:value})

			else:

				if event:

					event=False
					events.append(newEventDict)

		self.dictAMI=dictAMI
		self.events=events

	def getValue(self,key):

		try:

			value=self.dictAMI[key]
		except:

			value=""

		return value

			
