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
data_delay = 0.2

# how often to get environmental and picture
env_delay = 5

def main(downlink_queue,data_directory):
	print('Utility thread initialized...')
	downlink_queue.put(['UT','BU', 0])
	timer = 0
	while True:
		# gets and downlinks pressure system data
		pres_data = sensors.read_transducers()
		downlink_queue.put(pres_data)

		# executes every five seconds
		timer = timer + data_delay
		if timer >= env_delay:
			# gets list of downlink formatted data
			data_set = sensors.read_sensors()
			# downlinks each set of data
			for data in data_set:
				downlink_queue.put(data)
			# takes picture on cam 0 and 1
			#cameras.takePicture(data_directory)
			# resets timer
			timer = 0
		time.sleep(data_delay)
