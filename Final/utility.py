##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import time
from sensors import read_sensors, print_sensors

def main(downlink_queue,running,stage):
	downlink_queue.put(['UT','BU', 0])
	while running:
		# gets list of downlink formatted data
		data_set = read_sensors()
		# downlinks each set of data
		for data in data_set:
			downlink_queue.put(data)
		time.sleep(0.5)
