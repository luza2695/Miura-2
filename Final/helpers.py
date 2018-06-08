# stage change funcion
def changeStage(stage):
	return stage, time.time()

# switches solenoid based on which are enabled or disabled
def switchSolenoid(current_solenoid,solenoid_1_enabled,solenoid_2_enabled):
	if solenoid_1_enabled and solenoid_2_enabled:
		if current_solenoid == 1:
			current_solenoid = 2
		else:
			current_solenoid = 1
	elif solenoid_1_enabled:
		current_solenoid = 1
	elif solenoid_2_enabled:
		current_solenoid = 2
	else:
		current_solenoid = 0
	return current_solenoid