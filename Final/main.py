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
from heater import heaterPayload, heaterValve
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

##############################################################################
#Variables
maxInflationTime = 30
time_temp_start = 0
time_temp_end = 0
stage = 1

#pressure check loop
while running:
	uplink(serial)
	donwlink(serial)
	#if it is stage 1 (ascent) ...
	#	- Turn off camera
	#	- Do not run any of the pressure checks
	#	- Turn on heaters
	if stage == 1: #ascent stage 1 
		time_temp_start = time.time()


	#if it is stage 2 (inflation) ...
	#	- Starts when stage 1 or 5 is completed
	#	- Open solenoid valve
	#	- Motor given NO power
	#	- Close exhaust valve
	#	- Camera ON
	#	- Stops ...
	#		- when pressure has reached the maximum capacity
	#		- When the inflation timer has been reached 
	else if stage == 2: #infating // stage 2

	#if it is stage 3 (inflated) ...
	#	- Starts when inflation is completed
	#	- Close solenoid valve
	#	- Close Exhaust valve
	#	- Motor given NO power
	#	- Camera ON
	#	- Stops when the inflated timer is done
	else if stage == 3:
	
	#if it is stage 4 (deflating) ...
	#	- Starts when inflated timer has been completed
	#	- Close Solenoid valve
	#	- Open Exhaust valve
	#	- Motor ON
	#	- Camera ON
	#	- Stops when motor has fully retracted
	else if stage == 4:

	#if it is stage 5 (deflated) ...
	#	- Starts when deflation is completed
	#	- Close Solenoid Valve
	#	- Close Exhaust valve
	#	- Motor ON, but not moving (only torqued)
	#	- Camera ON
	#	- Stops when deflated timer is done
	else if stage == 5:

	#If it is stage 6 (emergency) ...
	#	- Starts when pressure > 0.8 atms
	#	- Close Solenoid Valve
	#	- Open Exhaust Valve
	#	- Motor OFF
	#	- Camera ON
	#	- Stops when pressure becomes less than 0.8 atm (stable)
	else if value > 0.8 or stage == 6: #atm


	#check data every 0.1 seconds
	time.sleep(0.1)
