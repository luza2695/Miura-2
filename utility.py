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
env_delay = 10

def main(downlink_queue,data_directory):
	print('Utility thread initialized...')
	downlink_queue.put(['UT','BU', 0])
	timer = 0
	while True:
		# executes every five seconds
		timer = timer + data_delay
		if timer >= env_delay:
			sensor_timer = time.time()
			# takes picture on cam 0 and 1
			cameras.takePicture(data_directory)
			# gets list of downlink formatted data
			data_set = sensors.read_sensors()
			# downlinks each set of data
			for data in data_set:
				downlink_queue.put(data)
			# resets timer
			timer = time.time() - sensor_timer
		time.sleep(data_delay)
