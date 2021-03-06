# Check to see if temp sensors are within normal operating temperatures
def check_temp(data):
	for i in range(len(data)):
		if i % 2 == 0:
			label = data[i] - 1
		else:
			value = data[i]
			if value > temp_max[label] or value < temp_min[label]:
				return True
	return False


# Determine temperature sensor identity
def temp_find(address):
	if address == camera_wall_1:
		return 1
	elif address == camera_wall_2:
		return 2
	elif address == camera_wall_3:
		return 3
	elif address == camera_wall_4:
		return 4
	elif address == temp_motor:
		return 5
	elif address == buck_converter:
		return 6
	elif address == ambient_internal:
		return 7
	elif address == ambient_external:
		return 8
	elif address == motor_driver:
		return 9

# Read temperature and downlink
def read_temp(downlink, temp_led):
	try:
		data = []
		for sensor in W1ThermSensor.get_available_sensors(): # Grab temp values from all available sensors in a round robin fashion
			data.append(temp_find(sensor.id))
			data.append(sensor.get_temperature())
		if check_temp(data):
			if not temp_led.is_set():
				GPIO.output(led_pin,True)
				temp_led.set()
		else:
			if temp_led.is_set():
				GPIO.output(led_pin,False)
				temp_led.clear()
		downlink.put(["SE", "T%i" % (len(data)/2), cs_str(data)]) # Send the packaged data packet to the downlink thread.
	except:
		pass


# Grab raw data from bus. Convert raw data to nice data.
def read_humi(downlink):
	try:
		bus.write_byte(0x40, 0xF5)
		time.sleep(0.3)
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		time.sleep(0.3)
		downlink.put(["SE", "HU", "{0:.2f}".format(humidity)])
	except:
		pass


# Grab raw data from bus. Convert raw data to nice data.
def read_pres(downlink):#downlink
	try:
		data = bus.read_i2c_block_data(0x60, 0x00, 4)
		pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16 # Use with humidity sensor?
		pressure = (pres / 4.0) / 1000.0
		downlink.put(["SE", "PR", "{0:.2f}".format(pressure)])
	except:
		pass
