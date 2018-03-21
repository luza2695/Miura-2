##################################################################
#Purpose:
#   - To create a prototype that displays the concept of operation
#for the software during the pressure stages
#   - Use LED's to indicate what valve/stage/time it is on
#Created: 3/13/2018
#Modified: -/-
#Miura 2: Prototype (proto.py)
#Project: Miura 2
##################################################################
#   -- Imports & Housing Keeping --

# Import code shared between threads
import serial
import uplink
from sys import platform

current_port = "/dev/ttyUSB0"
# Create serial object
ground = serial.Serial(port=current_port, #user input
			baudrate=4800, #user input
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1)

while True:
    uplink.main(ground)


