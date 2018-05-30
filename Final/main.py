#######################################################################
# Purpose: 
#	- To continuously check the pressure sensors
#	- To take in the uplink commands
#	- Control the feedback of the pressure
# Inputs:
#	- Pressure and temperature sensors
#	- Motor, heaters, pressure system
#	- Uplink
# Outputs:
#	- State (6 states)
#	- Uplink (only for camera use)
# Created: 5/1/2018
# Modified: 5/29/2018
# Miura2 - main.py
#######################################################################
# Imports:
import os
import threading
import time
import utility
from uplink import uplink
from downlink import downlink
#######################################################################

# start time for measuring time elapsed and for file naming
start_timestamp = time.time()
start_time = time.strftime('%b_%m_%H:%M:%S')

# creates directory where log file and data files will be saved
file_index = 0
while os.path.exists('/Desktop/Miura-2/Final/logfiles/datalog{}'.format(file_index)):
    file_index += 1
data_directory = '/Desktop/Miura-2/Final/logfiles/datalog{}'.format(file_index)
#os.mkdir(data_directory)

# sets up the log file, initialize as empty
log_filename = '{}/mission.log}'.format(data_directory)
log_lock = threading.Lock()
open(log_filename, 'w+').close()

# sets up downlink queue
downlink_queue = queue.Queue()
downlink_queue.put('Data Log {}'.format(file_index))
downlink_queue.put('Start Time: {}'.format(start_time))

# sets current pi usb port
current_port = "/dev/ttyUSB0"

# creates serial object for uplink and downlink
serial = serial.Serial(port=current_port,
                      baudrate=4800,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,
                      timeout=1)

# start utilty thread
utility_thread = threading.Thread(name=utility, args=(downlink_queue, log_filename, log_lock))
utility_thread.start()

# start checking uplink for commands
running = True
while(running):
	uplink(serial)
	donwlink(serial)

