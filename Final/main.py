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
# Modified: 6/7/2018
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
import solenoid
import cameras
#import lights
from helpers import changeStage, switchSolenoid
#######################################################################

#Variables
stage = 1
stage_start_time = time.time()
# gets start time of main thread
start_time = time.strftime('%m_%d_%Y_%H:%M:%S')

# creates log file
try: # checks log directory exists
    os.mkdir('datalogs')
except FileExistsError:
    # This directory should exist, just making sure
    pass
file_index = 0
while os.path.exists('datalogs/log{}'.format(file_index)):
    file_index += 1
data_directory = 'datalogs/log{}'.format(file_index)
os.mkdir(data_directory)

# Set up the log file, initialize as empty
log_filename = '{}/mission.log'.format(data_directory)
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
manual = False
solenoid_1_enabled = True
solenoid_2_enabled = True
current_solenoid = 1

# start utilty thread
utility_thread = threading.Thread(name='util',target=utility.main,args=(downlink_queue,running, stage),daemon=True)
utility_thread.start()

# pressure check loop
while running:
	#Start the uplink/downlink
	manual, stage, solenoid_1_enabled, solenoid_2_enabled = uplink.main(serial, downlink_queue, manual, stage, solenoid_1_enabled, solenoid_2_enabled)
	downlink.main(serial, downlink_queue, log_filename, stage)

	#Track the current time
	current_time = time.time()

	# checks if in manual mode
	if not manual:
		switchSolenoid(current_solenoid,solenoid_1_enabled,solenoide_2_enabled)
		#if it is stage 1 (ascent) ...
		#	- Turn off still and video cameras
		#	- Do not run any of the pressure checks
		#	- Turn on heaters
		#	- Lights OFF
		if stage == 1: #ascent stage 1
			#Turn on heaters
			#heater.solenoid_heater(True)
			#heater.payload_heater(True)

			#Turn off Cameras
			#cameras.stillCameras()
			#cameras.videoCamera()

			#conditionals ...
			#	- after 4 hours into flight
			if (current_time-stage_start_time) >= 14400:
				stage, stage_start_time = changeStage(2)
		#if it is stage 2 (inflation) ...
		#	- Starts when stage 1 or 5 is completed
		#	- Open solenoid valve
		#	- Motor given NO power
		#	- Close exhaust valve
		#	- Video and still cameras ON
		#	- Lights ON
		#	- Stops ...
		#		- when pressure has reached the maximum capacity
		#		- When the inflation timer has been reached 
		elif stage == 2: #inflating // stage 2
			#Lights ON
			#lights.lights(1)

			#Read pressure
			value2 = sensors.read_pressure_system()

			#Open solenoid valve and Motor OFF
			solenoid.openPressurize(current_solenoid)

			#Close exhaust valve
			solenoid.closeExhaust()

			#Video and still Cameras ON
			#cameras.stillCameras()
			#cameras.videoCamera()

			#EMERGENCY CONDITION (STAGE 6)
			if value2 >= 0.8: #atm
				stage == 6
			# Conditionals:
			#	-if pressure is 0.55 or greater
			#	-if 1 min goes by
			elif value2 >= 0.55 or (current_time-stage_start_time) >= 60: #atm
			 	stage, stage_start_time = changeStage(3)
			 	solenoid.closePressurize(1)



		#if it is stage 3 (inflated) ...
		#	- Starts when inflation is completed
		#	- Close solenoid valve
		#	- Close Exhaust valve
		#	- Motor given NO power
		#	- Still Cameras ON // video camera OFF
		#	- Stops when the inflated timer is done
		#	- Lights ON
		elif stage == 3:
			#Lights ON
			#lights.lights(1)

			#read pressure
			value3 = sensors.read_pressure_system()

			#close solenoid valve and motor OFF
			solenoid.closePressurize(current_solenoid)

			#close exhaust
			solenoid.closeExhaust()

			#Still cameras ON // video camera OFF
			#cameras.stillCameras(True)
			#cameras.videoCamera(False)

			#EMERGENCY CONDITION (STAGE 6)
			if value3 >= 0.8: #atm
	            		stage == 6
			#Conditionals ...
			#	-After 10 min has been passed
			#
			elif (current_time-stage_start_time) >= 600:
	         		stage, stage_start_time = changeStage(4)

		#if it is stage 4 (deflating) ...
		#	- Starts when inflated timer has been completed
		#	- Close Solenoid valve
		#	- Open Exhaust valve
		#	- Motor ON
		#	- Video and Still Cameras ON
		#	- Stops when motor has fully retracted
		#	- Lights ON
		elif stage == 4:
			#Lights ON
			#lights.lights(1)

			#read pressure from tranducer
			value4 = sensors.read_pressure_system()

			#Close solenoid valve
			solenoid.closePressurize(current_solenoid)

			#open exhaust and motor ON
			solenoid.openExhaust()

			#Video and Still Cameras ON
			#cameras.stillCameras()
			#cameras.videoCamera()

			#EMERGENCY CONDITION (STAGE 6)
			if value4 >= 0.8: #atm
	            		stage == 6
			#Conditionals ...
			#	-once motor completes the theoretical revs around
			#	-1 min has passed
			#	-pressure exceeds 0.55 or lower than 0.3
			elif (stage_start_time - current_time) >= 60 or value4 >= 0.55 or value <= 0.3:
	        		stage, stage_start_time = changeStage(5)

		#if it is stage 5 (deflated) ...
		#	- Starts when deflation is completed
		#	- Close Solenoid Valve
		#	- Close Exhaust valve
		#	- Motor ON, but not moving (only torqued)
		#	- Still Cameras ON // video camera OFF
		#	- Stops when deflated timer is done
		#	- Lights ON
		elif stage == 5:
			#Lights ON
			#lights.lights(1)

			#Close solenoid valve
			solenoid.closePressurize(current_solenoid)

			#Close exhaust valve
			solenoid.closeExhaust()

			#Still cameras ON // video camera OFF
			#cameras.stillCameras()
			#cameras.videoCamera()


			#EMERGENCY CONDITION (STAGE 6)
			if value5 >= 0.8: #atm
	        		stage == 6
			#Conditionals ...
			#	-when 3 minutes passes by
			elif (stage_start_time - current_time) >= 180:
	        		stage, stage_start_time = changeStage(2)
	        		#let the celebration begin
	        		#lights.lights(2) & omxplayer -o local example.mp3

		#If it is stage 6 (emergency) ...
		#	- Starts when pressure > 0.8 atms
		#	- Close Solenoid Valve
		#	- Open Exhaust Valve
		#	- Motor OFF
		#	- Camera ON
		#	- Stops when pressure becomes less than 0.8 atm (stable)
		#	- Lights ON
		elif stage == 6: #atm
			#Lights ON
			#lights.lights(1)

			#Close solenoid valve
			solenoid.closePressurize(current_solenoid)

			#Open exhaust valve
			solenoid.openExhaust()

			#Still Cameras ON
			#cameras.stillCameras()

	#check data every 0.5 seconds
	time.sleep(0.5)
