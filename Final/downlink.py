##################################################################
# Miura 2: Downlink Code (downlink.py)
# Created: 3/13/2018
# Modified: 5/29/2018
# Purpose: Downlink data and write to log file
##################################################################
import serial
import time
from zlib import adler32

def main(serial, downlink_queue):#, log_filename, log_lock):
	if not downlink_queue.empty():
		message = downlink_queue.get() # gets message from downlink queue
		print(message)
		sender, data_type, data = message[0], message[1], str(message[2]) # isolates into sender of message, data type, and the data
		data_length = len(data) # calculates length of data
		encoded_data = data.encode() # encodes data
		checksum = adler32(encoded_data) # calculates checksum
		current_time = time.time() # gets current time
		packet = "\x01CU MI %s %s %.2f %i %i\x02" % (sender, data_type, current_time, data_length, checksum) + " " + data + "\x03\n"
		print(packet)
		#serial.write(packet) # writes message to serial
	return