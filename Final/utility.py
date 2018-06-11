##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import time
import sensors
import cameras

# how often to get data
data_delay = 0.5

# how often to get pictures
pic_delay = 5
pic_timer = 0

def main(downlink_queue,data_directory):
	print('Utility thread initialized...')
	downlink_queue.put(['UT','BU', 0])
	while True:
		# gets list of downlink formatted data
		data_set = sensors.read_sensors()
		# downlinks each set of data
		for data in data_set:
			downlink_queue.put(data)

		# takes pic every 5 seconds
		pic_timer += data_delay
		if pic_timer >= 5:
			pic_timer = 0
			cameras.takePicture(data_directory)

		time.sleep(data_delay)
