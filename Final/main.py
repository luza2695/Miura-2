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
# Tasks:
#	- Check if main is okay logically
#	- Motor code --> DC brushless
#	- Make the downlink horizontal
#	- Motor ON - Torqued only
# Created: 5/1/2018
# Modified: 6/1/2018
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
import heater
import sensors
#import solenoid
import cameras
#######################################################################

#Variables
stage = 1
stage_start_time = time.time()
# gets start time of main thread
start_time = time.strftime('%m_%d_%Y_%H:%M:%S')

# creates log file
try: # checks log directory exists
    os.mkdir('Log Data')
except FileExistsError:
    # This directory should exist, just making sure
    pass
file_index = 0
while os.path.exists('home/pi/Desktop/Miura-2/Miura-2/Final/Log Data/mission{}.log'.format(file_index)):
	file_index += 1
log_filename = 'home/pi/Desktop/Miura-2/Miura-2/Final/Log Data/mission{}.log'.format(file_index)
open(log_filename, 'w+').close()

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
	#Start the uplink/downlink
	uplink.main(serial, downlink_queue)
	downlink.main(serial, downlink_queue, log_filename, stage)

	#Track the current time
	current_time = time.time()
	#if it is stage 1 (ascent) ...
	#	- Turn off still and video cameras
	#	- Do not run any of the pressure checks
	#	- Turn on heaters
	if stage == 1: #ascent stage 1
		#Turn on heaters
		#heater.solenoid_heater(True)
		#heater.payload_heater(True)

		#Turn off Cameras
		#cameras.stillCameras(False)
		#cameras.videoCamera(True)

		#conditionals ...
		#	- after 4 hours into flight
		if (current_time-stage_start_time) >= 14400:
			stage, stage_start_time = stagechange(2)
	#if it is stage 2 (inflation) ...
	#	- Starts when stage 1 or 5 is completed
	#	- Open solenoid valve
	#	- Motor given NO power
	#	- Close exhaust valve
	#	- Video and still cameras ON
	#	- Stops ...
	#		- when pressure has reached the maximum capacity
	#		- When the inflation timer has been reached 
	elif stage == 2: #infating // stage 2
		#Read pressure
		#value2 = sensors.read_pressure_system()

		#Open solenoid valve and Motor OFF
		#solenoid.openPressurize(1)

		#Close exhaust valve
		#solenoid.closeExhaust()

		#Video and still Cameras ON
		#cameras.stillCameras(True)
		#cameras.videoCamera(True)

		# Conditionals:
		#	-if pressure is 0.55 or greater
		#	-if 1 min goes by
		if value2 >= 0.55 or (current_time-stage_start_time) >= 60: #atm
		 	stage, stage_start_time = stagechange(3)
		 	#solenoid.closePressurize(1)

		#EMERGENCY CONDITION (STAGE 5)
		elif value2 >= 0.8: #atm
			stage == 6

	#if it is stage 3 (inflated) ...
	#	- Starts when inflation is completed
	#	- Close solenoid valve
	#	- Close Exhaust valve
	#	- Motor given NO power
	#	- Still Cameras ON // video camera OFF
	#	- Stops when the inflated timer is done
	elif stage == 3:
		#read pressure
		#value3 = sensors.read_pressure_system()

		#close solenoid valve and motor OFF
		#solenoid.closePressurize(1)

		#close exhaust
		#solenoid.closeExhaust()

		#Still cameras ON // video camera OFF
		#cameras.stillCameras(True)
		#cameras.videoCamera(False)

		#Conditionals ...
		#	-After 10 min has been passed
		#
		if (current_time-stage_start_time) >= 600:
         		stage, stage_start_time = stagechange(4)

		#EMERGENCY CONDITION (STAGE 6)
		elif value3 >= 0.8: #atm
            		stage == 6

	#if it is stage 4 (deflating) ...
	#	- Starts when inflated timer has been completed
	#	- Close Solenoid valve
	#	- Open Exhaust valve
	#	- Motor ON
	#	- Video and Still Cameras ON
	#	- Stops when motor has fully retracted
	elif stage == 4:
		#read pressure from tranducer
		#value4 = sensors.read_pressure_system()

		#Close solenoid valve
		# solenoid.closePressurize(1)

		#open exhaust and motor ON
		#solenoid.openExhaust()

		#Video and Still Cameras ON
		#cameras.stillCameras(True)
		#cameras.videoCamera(True)

		#Conditionals ...
		#	-once motor completes the theoretical revs around
		#	-1 min has passed
		#	-pressure exceeds 0.55 or lower than 0.3
		if (stage_start_time - current_time) >= 60 or value4 >= 0.55 or value <= 0.3:
        		stage, stage_start_time = stagechange(5)

		#EMERGENCY CONDITION (STAGE 6)
		elif value4 >= 0.8: #atm
            		stage == 6

	#if it is stage 5 (deflated) ...
	#	- Starts when deflation is completed
	#	- Close Solenoid Valve
	#	- Close Exhaust valve
	#	- Motor ON, but not moving (only torqued)
	#	- Still Cameras ON // video camera OFF
	#	- Stops when deflated timer is done
	elif stage == 5:
		#Close solenoid valve
		#solenoid.closePressurize()

		#Close exhaust valve
		#solenoid.closeExhaust()

		#Motor ON - TORQUED
		#DO THIS LATER!

		#Still cameras ON // video camera OFF
		#cameras.stillCameras(True)
		#cameras.videoCamera(False)

		#Conditionals ...
		#	-when 3 minutes passes by
		if (stage_start_time - current_time) >= 180:
        		stage, stage_start_time = stagechange(2)

		#EMERGENCY CONDITION (STAGE 6)
		elif value5 >= 0.8: #atm
        		stage == 6

	#If it is stage 6 (emergency) ...
	#	- Starts when pressure > 0.8 atms
	#	- Close Solenoid Valve
	#	- Open Exhaust Valve
	#	- Motor OFF
	#	- Camera ON
	#	- Stops when pressure becomes less than 0.8 atm (stable)
	elif stage == 6: #atm
		#Close solenoid valve
		#solenoid.closePressurize()

		#Open exhaust valve
		#solenoid.openExhaust()

		#Motor OFF
		#DO THIS LATER!

		#Still Cameras ON
		#cameras.stillCameras(True)
		pass
	#check data every 0.5 seconds
	time.sleep(0.5)

# stage change funcion
def stagechange(stage):
	return stage, time.time()
