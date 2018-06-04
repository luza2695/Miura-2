##################################################################
# Miura 2: Downlink Code (downlink.py)
# Created: 3/13/2018
# Modified: 5/29/2018
# Purpose: Downlink data and write to log file
##################################################################
import serial
import time
from zlib import adler32

def main(serial, downlink_queue, log_filename, stage):
	if not downlink_queue.empty():
		message = downlink_queue.get() # gets message from downlink queue
		sender, data_type, data = message[0], message[1], str(message[2]) # isolates into sender of message, data type, and the data
		checksum = adler32(data.encode()) # calculates checksum
		current_time = time.time() # gets current time
		packet = '\x01CU MI2 %s %s %.2f %i %i\x02' % (sender, data_type, current_time, checksum, stage) + ' ' + data + '\x03\n'
		print(packet)
		with open(log_filename, 'a') as log: # opens log file
			log.write(message) # writes to log file
			serial.write(packet.encode()) # writes message to serial
	return
