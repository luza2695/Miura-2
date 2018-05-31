##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import time
import sensors

# how often to get data
time_delay = 0.5

def main(downlink_queue,running,stage):
	downlink_queue.put(['UT','BU', 0])
	while running:
		# gets list of downlink formatted data
		data_set = sensors.read_sensors()
		# downlinks each set of data
		for data in data_set:
			downlink_queue.put(data)
		time.sleep(time_delay)
