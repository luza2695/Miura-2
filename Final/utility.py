##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import time
from sensors import read_sensors, print_sensors

def main(downlink_queue,running):
	downlink_queue.put(['UT','BU', 0])
	while running:
		pressure, humidity, temperature = read_sensors()
		downlink_queue.put(['SE','PR', pressure])
		downlink_queue.put(['SE','HU', humidity])
		downlink_queue.put(['SE','TE', temperature])
		time.sleep(0.5)
