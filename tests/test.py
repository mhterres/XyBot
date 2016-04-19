#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time

sys.path.insert(1,'%s/../' % os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1,'%s/../libs' % os.path.dirname(os.path.realpath(__file__)))

from libs.config import Config
from libs.ami import AMI

cfg=Config()

ami=AMI(cfg.ami_srv,cfg.ami_port,cfg.ami_user,cfg.ami_secret)

#events=ami.sendAction([("Action","QueueSummary")])
#events=ami.sendAction([("Action","CoreStatus")])
#events=ami.sendAction([("Action","CoreSettings")])
events=ami.sendAction([("Action","QueueStatus"),("Queue","myqueue")])
#events=ami.sendAction([("Action","QueueStatus"),("Queue","myqueue"),("Interface","PJSIP/1000")])

print ami.lastDictAMI
print events

