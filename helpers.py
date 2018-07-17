##################################################################
# Miura 2: Helper Functions (helper.py)
# Created: 5/29/2018
# Modified: 6/30/2018
# Purpose: Helper functions for use in main thread
##################################################################
import time

# stage change funcion
def changeStage(stage):
	return stage, time.time(), False


# switches solenoid based on which are enabled or disabled
def switchSolenoid(current_solenoid,solenoid_1_enabled,solenoid_2_enabled,tank1,tank2):
	if solenoid_1_enabled and solenoid_2_enabled and tank1>=5 and tank2>=5:
		if current_solenoid == 1:
			current_solenoid = 2
		else:
			current_solenoid = 1
		print('Auto change to valve {}...'.format(current_solenoid))
	elif solenoid_1_enabled and tank1>=7.5:
		current_solenoid = 1
		print('Valve 2 disabled. Auto change to valve {}...'.format(current_solenoid))
	elif solenoid_2_enabled and tank2>=7.5:
		current_solenoid = 2
		print('Valve 1 disabled. Auto change to valve {}...'.format(current_solenoid))
	else:
		current_solenoid = 0
		print('Both valves disabled.')
	return current_solenoid
