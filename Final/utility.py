# imports
import serial
import time
import downlink

def utility(downlink_queue, log_filename, log_lock):
	for i in range(0,4):
		testDownlink.downlink(bytes(str(i),'utf-8'))
