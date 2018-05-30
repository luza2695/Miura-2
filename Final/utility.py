##################################################################
# Miura 2: Utility Thread (utility.py)
# Created: 5/29/2018
# Modified: 5/30/2018
# Purpose: Downlink data and write to log file
##################################################################

import time
from sensors import read_sensors, print_sensors

def main(downlink_queue):
	current_time = time.strftime('%b_%m_%H:%M:%S')
	print('Starting utility thread: {}'.format(current_time))
	while running:
		print_sensors()
		time.sleep(0.5)
