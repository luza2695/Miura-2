##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import serial
import time
from sensors import read_sensors, print_sensors

def utility(downlink_queue):
	while True:
		print_sensors()
		time.sleep(0.5)
