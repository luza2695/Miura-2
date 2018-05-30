##################################################################
# Miura 2: Downlink Code (downlink.py)
# Created: 3/13/2018
# Modified: 5/29/2018
# Purpose: Downlink data and write to log file
##################################################################

def downlink(serial, downlink_queue, log_filename, log_lock):
	while True:
		while not downlink_queue.empty():
			message = downlink_queue.get() + '\n'
			serial.write(message.encode())

			with log_lock:
				with open(log_filename, 'a') as f:
					f.write(message)

			print(message)

		time.sleep(1)