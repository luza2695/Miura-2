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
import queue
import serial
import utility
import uplink
import downlink
#import sched
import heater #heaterPayload, heaterValve
import sensors
import solenoid
#######################################################################

#Variables
stage = 1
stage_start_time = time.time()
# gets start time of main thread
start_time = time.strftime('%b_%m_%H:%M:%S')

# creates directory where log file and data files will be saved
file_index = 0
# while os.path.exists('/Desktop/Miura-2/Final/logfiles/datalog{}'.format(file_index)):
# 	file_index += 1
# data_directory = '/Desktop/Miura-2/Final/logfiles/datalog{}'.format(file_index)
#os.mkdir(data_directory)

# sets up the log file, initialize as empty
# log_filename = '{}/mission.log}'.format(data_directory)
# log_lock = threading.Lock()
# open(log_filename, 'w+').close()

# sets up downlink queue
downlink_queue = queue.Queue()
downlink_queue.put(['MA', 'BU', 0])

# sets current pi usb port
current_port = "/dev/ttyUSB0"

# creates serial object for uplink and downlink
serial = serial.Serial(port=current_port,
					  baudrate=4800,
					  parity=serial.PARITY_NONE,
					  stopbits=serial.STOPBITS_ONE,
					  bytesize=serial.EIGHTBITS,
					  timeout=1)

# clears the serial communication channel
serial.flushInput() 

running = True

# start utilty thread
utility_thread = threading.Thread(name='util',target=utility.main,args=(downlink_queue,running, stage),daemon=True)
utility_thread.start()

# pressure check loop
while running:
	uplink.main(serial, downlink_queue)
	downlink.main(serial, downlink_queue)
	
	current_time = time.time()
	#if it is stage 1 (ascent) ...
	#	- Turn off camera
	#	- Do not run any of the pressure checks
	#	- Turn on heaters
	if stage == 1: #ascent stage 1 
		#Turn on heaters
		#heater.solenoid_heater(True)
		#heater.payload_heater(True)

		#Turn on Camera
		#DO THIS LATER

		#conditionals ...
		#	- after 4 hours into flight
		if (current_time-stage_start_time) >= 14400 :
			stage, stage_start_time = stagechange(2)


	#if it is stage 2 (inflation) ...
	#	- Starts when stage 1 or 5 is completed
	#	- Open solenoid valve
	#	- Motor given NO power
	#	- Close exhaust valve
	#	- Camera ON
	#	- Stops ...
	#		- when pressure has reached the maximum capacity
	#		- When the inflation timer has been reached 
	elif stage == 2: #infating // stage 2
		#Read pressure
		value2 = sensors.read_pressure_system()

		#Open solenoid valve and Motor OFF
		#solenoid.openPressurize()

		#Close exhaust valve
		#solenoid.closeExhaust()

		#Camera ON
		#DO THIS LATER

		# Conditionals:
		#	-if pressure is 0.75 or greater
		#	-if __ (time) goes by
		# if value2 >= 0.75 or (current_time-stage_start_time) >= 300: #atm
		# 	stage, stage_start_time = stagechange(3)
		# 	solenoid.closePressurize()

	#if it is stage 3 (inflated) ...
	#	- Starts when inflation is completed
	#	- Close solenoid valve
	#	- Close Exhaust valve
	#	- Motor given NO power
	#	- Camera ON
	#	- Stops when the inflated timer is done
	elif stage == 3:
		#read pressure
		value3 = sensors.read_pressure_system()

		#close solenoid valve and motor OFF
		#solenoid.closePressurize()

		#close exhaust
		#solenoid.closeExhaust()

		#camer ON
		#DO THIS LATER

		#Conditionals ...
		#	-After __ hours has been passed
		#	- 
		# if (current_time-stage_start_time) >= 3600:
  #       	stage, stage_start_time = stagechange(4)

	#if it is stage 4 (deflating) ...
	#	- Starts when inflated timer has been completed
	#	- Close Solenoid valve
	#	- Open Exhaust valve
	#	- Motor ON
	#	- Camera ON
	#	- Stops when motor has fully retracted
	elif stage == 4:
		#read pressure from tranducer
		value4 = sensors.read_pressure_system()

		#Close solenoid valve
		# solenoid.closePressurize()

		#open exhaust and motor ON
		#solenoid.openExhaust()

		#Camera ON
		#DO THIS LATER!

		#Conditionals ...
		#	-once motor completes the theoretical revs around
		#	-30 min has passed
		#if False:
        	#stage, stage_start_time = stagechange(3)


	#if it is stage 5 (deflated) ...
	#	- Starts when deflation is completed
	#	- Close Solenoid Valve
	#	- Close Exhaust valve
	#	- Motor ON, but not moving (only torqued)
	#	- Camera ON
	#	- Stops when deflated timer is done
	elif stage == 5:
		pass
	
	#If it is stage 6 (emergency) ...
	#	- Starts when pressure > 0.8 atms
	#	- Close Solenoid Valve
	#	- Open Exhaust Valve
	#	- Motor OFF
	#	- Camera ON
	#	- Stops when pressure becomes less than 0.8 atm (stable)
	elif value > 0.8 or stage == 6: #atm
		pass

	#check data every 0.1 seconds
	time.sleep(0.1)

# stage change funcion
def stagechange(stage):
	return stage, time.time()
