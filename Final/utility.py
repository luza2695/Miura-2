##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import serial
import time
import downlink

def utility(downlink_queue, log_filename, log_lock):
	for i in range(0,4):
		testDownlink.downlink(bytes(str(i),'utf-8'))
