##################################################################
# Miura 2: Main Thread (main.py)
# Created: 5/1/2018
# Modified: 6/30/2018
# Purpose: Control pressurization cycles, uplink, and downlink
##################################################################
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
import RPi.GPIO as GPIO
import motor
#import lights
import atexit
from helpers import changeStage, switchSolenoid

#Indicator LED Startup
stage_1 = 38
stage_2 = 35
stage_3 = 36
stage_4 = 33
stage_5 = 32
emergency_pressure_led = 31
emergency_temperature_led = 29

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(stage_1, GPIO.OUT)
GPIO.setup(stage_2, GPIO.OUT)
GPIO.setup(stage_3, GPIO.OUT)
GPIO.setup(stage_4, GPIO.OUT)
GPIO.setup(stage_5, GPIO.OUT)
GPIO.setup(emergency_pressure_led, GPIO.OUT)
GPIO.setup(emergency_temperature_led, GPIO.OUT)


# important variables for operation
cycle_start_delay = 10 # 10800 # (3 hours)
inflation_time = 120 # (2 minutes)
sustention_time = 60 # (10 minutes)
retraction_time = 180 # (3 minutes)
deflation_time = 30 # (30 minutes)
main_delay = 0.2 # seconds
emergency_pressure = 15 # psi
standard_pressure = 7.5 # psi

# main thread has started
print('Main thread initialized...')

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

# set up the log file, initialize as empty
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

# setting up functions to run at exit
atexit.register(motor.turnOffMotors)
atexit.register(sensors.cleanup)

# start utilty thread
utility_thread = threading.Thread(name = 'util', target = utility.main, args = (downlink_queue,data_directory), daemon = True)
utility_thread.start()

# sets variables for main loop operation
running = True
manual = False
solenoid_1_enabled = True
solenoid_2_enabled = True
current_solenoid = 2
current_cycle = 1
pressurization_counter = 0
emergency_counter = 0
transducer_downlink_counter = 0
stage, stage_start_time, tasks_completed  = changeStage(1)

# pressure check loop
while running:

	# downlink transducer data every 5 loops
	transducer_downlink_counter += 1
	if transducer_downlink_counter >= 5:
		transducer_data = sensors.read_transducers()
		downlink_queue.put(transducer_data)
		transducer_downlink_counter = 0

	# uplink and downlink
	manual, stage, stage_start_time, solenoid_1_enabled, solenoid_2_enabled, tasks_completed = uplink.main(serial, downlink_queue, data_directory, manual, stage, stage_start_time, solenoid_1_enabled, solenoid_2_enabled, tasks_completed)
	downlink.main(serial, downlink_queue, log_filename, stage, current_cycle)

	# checks if in manual mode
	if not manual:

		# get current time
		current_time = time.time()

		# STAGE 1: ASCENT
		if stage == 1:

			# read pressure to check for end of inflation
			tank1,tank2,main = sensors.read_pressure_system()

			# if pressure exceeds 10 psi
			if main >= emergency_pressure:
				emergency_counter += 1
				if emergency_counter >= 5:
					# switch to emergency stage
					stage, stage_start_time, tasks_completed = changeStage(6)
					emergency_counter = 0
			else:
				emergency_counter = 0

			# if time to start cycle
			if (current_time-stage_start_time) >= cycle_start_delay:

				# switch to stage 2
				stage, stage_start_time, tasks_completed = changeStage(2)
				#GPIO.output(stage_1, False)
				continue

			# perform one time tasks
			if (not tasks_completed):
				# open exhaust
				solenoid.openExhaust()

				#Turn on LED for stage 1
				#GPIO.output(stage_1, True)

				#Turn off emergency led
				#GPIO.output(emergency_pressure_led, False)

				# close both pressurize
				solenoid.closePressurize(1)
				solenoid.closePressurize(2)

				# mark tasks at completed
				tasks_completed = True

			# checks heater temperatures
			temp_data = sensors.read_temp()
			# solenoid control
			if temp_data[0] > 30 or temp_data[1] > 30 or temp_data[2] > 30:
				heater.solenoid_heater(False)
			else:
				heater.solenoid_heater(True)
			# regulator control
			if temp_data[3] > 30 or temp_data[4] > 30:
				heater.regulator_heater(False)
			else:
				heater.regulator_heater(True)

		# STAGE 2: INFLATION
		elif stage == 2:

			# read pressure to check for end of inflation
			tank1,tank2,main = sensors.read_pressure_system()

			# if pressure exceeds 10 psi
			if main >= emergency_pressure:
				emergency_counter += 1
				if emergency_counter >= 5:
					# switch to emergency stage
					stage, stage_start_time, tasks_completed = changeStage(6)
					emergency_counter = 0
			# if reaches maximum inflation time
			elif (current_time-stage_start_time) >= inflation_time:

				# close current pressurize valve
				solenoid.closePressurize(current_solenoid)
				pressurization_counter = 0

				# switch to stage 3
				stage, stage_start_time, tasks_completed = changeStage(3)
				#GPIO.output(stage_2, False)
				continue

			# if pressure reaches 7.5 psi
			elif main >= standard_pressure:
				emergency_counter = 0
				pressurization_counter += 1
				if pressurization_counter >= 3:
					# close current pressurize valve
					solenoid.closePressurize(current_solenoid)
					pressurization_counter = 0

					# switch to stage 3
					stage, stage_start_time, tasks_completed = changeStage(3)
					continue
			else:
				emergency_counter = 0
				pressurization_counter = 0



			# perform one time tasks
			if (not tasks_completed):

				#Turn on LED for stage 2
				#GPIO.output(stage_2, True)

				#Turn off emergency led
				#GPIO.output(emergency_pressure_led, False)

				# heaters on
				heater.solenoid_heater(False)
				heater.regulator_heater(False)

				# switch active solenoid
				current_solenoid = switchSolenoid(current_solenoid,solenoid_1_enabled,solenoid_2_enabled,tank1,tank2)

				# lights on
				#lights.lights_on()

				# start video
				#cameras.takeVideo(data_directory)

				# close exhaust valve
				solenoid.closeExhaust()

				# open current pressurize valve (and turn motor off)
				solenoid.openPressurize(current_solenoid)

				# mark tasks as completed
				tasks_completed = True


		# STAGE 3: INFLATED
		elif stage == 3:

			# read pressure to check for emergency
			tank1,tank2,main = sensors.read_pressure_system()

			# if pressure exceeds 10 psi
			if main >= emergency_pressure:
				emergency_counter += 1
				if emergency_counter >= 5:
					# switch to emergency stage
					stage, stage_start_time, tasks_completed = changeStage(6)
					emergency_counter = 0

			# if in the first 10 cycles
			elif current_cycle <= 10:
				# if sustention time has passed
				if (current_time-stage_start_time) >= sustention_time:
					# switch to stage 4
					stage, stage_start_time, tasks_completed = changeStage(4)
					#GPIO.output(stage_3, False)
					continue

			# if after the 10th cycle
			elif current_cycle > 10:
				# if pressure drops below 4.4 psi
				if main < 4.4:
					pressurization_counter += 1
					if pressurization_counter >= 5:
						# switch to stage 4
						stage, stage_start_time, tasks_completed = changeStage(4)
						pressurization_counter = 0
						continue
				else:
					pressurization_counter = 0
			else:
				emergency_counter = 0

			# perform one time tasks
			if (not tasks_completed):

				# lights on
				#lights.lights_on()

				#turn on LED for stage 3
				#GPIO.output(stage_3, True)

				#Turn off emergency led
				#GPIO.output(emergency_pressure_led, False)

				# close both pressurize
				solenoid.closePressurize(1)
				solenoid.closePressurize(2)

				# close exhaust
				solenoid.closeExhaust()

				# mark tasks as completed
				tasks_completed = True

		# STAGE 4: DEFLATING
		elif stage == 4:

			# read pressure to check for emergency
			tank1,tank2,main = sensors.read_pressure_system()

			# if pressure exceeds 10 psi
			if main >= emergency_pressure:
				emergency_counter += 1
				if emergency_counter >= 5:
					# switch to emergency stage
					stage, stage_start_time, tasks_completed = changeStage(6)
					emergency_counter = 0

			# if retraction time has passed
			elif (current_time - stage_start_time) >= retraction_time:

				# switch to stage 5
				stage, stage_start_time, tasks_completed = changeStage(5)
				#GPIO.output(stage_4, False)
				continue
			else:
				emergency_counter = 0

			# perform one time tasks
			if (not tasks_completed):

				# lights on
				#lights.lights_on()

				# start video
				#cameras.takeVideo(data_directory)

				#Turn on LED to stage 4
				#GPIO.output(stage_4, True)

				#Turn off emergency led
				#GPIO.output(emergency_pressure_led, False)

				# close both pressurize
				solenoid.closePressurize(1)
				solenoid.closePressurize(2)

				# open exhaust valve
				solenoid.openExhaust()

				# start motor thread
				motor_thread = threading.Thread(name = 'motor', target = motor.main, args = (), daemon = True)
				motor_thread.start()

				# mark tasks as completed
				tasks_completed = True

		# STAGE 5: DEFLATED
		elif stage == 5:

			# read pressure to check for emergency
			tank1,tank2,main = sensors.read_pressure_system()

			# if pressure exceeds 10 psi
			if main >= emergency_pressure:
				emergency_counter += 1
				if emergency_counter >= 5:
					# switch to emergency stage
					stage, stage_start_time, tasks_completed = changeStage(6)
					emergency_counter = 0

			# if deflation time has passed
			elif (current_time - stage_start_time) >= deflation_time:

				#let the celebration begin
				#lights.epilepsy()

				# & omxplayer -o local example.mp3

				# downlink cycle complete
				downlink_queue.put(['CY','CP','{}'.format(current_cycle)])

				# increment current cycle
				current_cycle += 1

				# switch to stage 2
				stage, stage_start_time, tasks_completed = changeStage(2)
				#GPIO.output(stage_5, False)
				continue
			else:
				emergency_counter = 0

			# perform one time tasks
			if (not tasks_completed):

				# lights on
				#lights.lights_on()

				#Turn LED FOR STAGE 5
				#GPIO.output(stage_5, True)

				#Turn off emergency led
				#GPIO.output(emergency_pressure_led, False)

				# close both pressurize
				solenoid.closePressurize(1)
				solenoid.closePressurize(2)

				# close exhaust valve
				solenoid.closeExhaust()

				# mark tasks as completed
				tasks_completed = True

		# STAGE 6: EMERGENCY
		elif stage == 6: #atm

			# perform one time tasks
			if (not tasks_completed):

				# lights on
				#lights.lights_on()

				#Turn LED FOR STAGE 5
				#GPIO.output(emergency_pressure_led, True)

				# close both pressurize
				solenoid.closePressurize(1)
				solenoid.closePressurize(2)

				# open exhaust valve
				solenoid.openExhaust()

				# downlink cycle emergency
				downlink_queue.put(['CY','EM','{}'.format(current_cycle)])

				# increment current cycle
				current_cycle += 1

				# put in manual mode
				manual = True

				# mark tasks as completed
				tasks_completed = True

	# restart loop after time delay
	time.sleep(main_delay)
