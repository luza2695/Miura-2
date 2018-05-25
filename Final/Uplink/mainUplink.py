##################################################################
# Purpose:
#   - Demonstrate successful uplink and execution of commands
# Created: 3/13/2018
# Modified: 3/21/2018
#
# Project: Miura 2 (Prototype)
##################################################################

# imports
import serial
import uplink

# sets current pi usb port
current_port = "/dev/ttyUSB0"

# Create serial object
ground = serial.Serial(port=current_port,
			baudrate=4800,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1)

# intializes loop to detect uplink
while True:
    uplink.main(ground)
