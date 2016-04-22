#!/usr/bin/python
# -*- coding: utf-8 -*-

# sippeerstatus.py
# return the status of an sip perr
#
# syntax: sippeerstatus.py <peer name>

import os
import sys
import time

sys.path.insert(1,'%s/../../' % os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1,'%s/../../libs' % os.path.dirname(os.path.realpath(__file__)))

from libs.config import Config
from libs.ami import AMI

cfg=Config()

try:

    sip = sys.argv[1]
except:

    print "You need to inform name of the SIP peer."
    sys.exit(1)

ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

events=ami.sendAction([("Action","Sippeerstatus"),("Peer",sip)])

returnmsg="Unreacheable"

for event in events:

    try:

        if event['Event']=="PeerStatus":

            try:

                returnmsg=event['PeerStatus']
		break
            except:
                pass
    except:

        pass

print returnmsg.strip()

