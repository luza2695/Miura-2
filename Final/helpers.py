import time

# stage change funcion
def changeStage(stage, current_solenoid):
	if stage == 2:
		current_solenoid = switchSolenoid()
	return stage, time.time(), current_solenoid


# switches solenoid based on which are enabled or disabled
def switchSolenoid(current_solenoid,solenoid_1_enabled,solenoid_2_enabled):
	if solenoid_1_enabled and solenoid_2_enabled:
		if current_solenoid == 1:
			current_solenoid = 2
		else:
			current_solenoid = 1
		print('Switching to valve {}'.format(current_solenoid))
	elif solenoid_1_enabled:
		current_solenoid = 1
		print('Valve 2 disabled')
		print('Switching to valve {}'.format(current_solenoid))
	elif solenoid_2_enabled:
		current_solenoid = 2
		print('Valve 1 disabled')
		print('Switching to valve {}'.format(current_solenoid))
	else:
		current_solenoid = 0
		print('Both valves disabled')
	return current_solenoid
