#######################################################################
# Purpose: 
#	- To continuously check the pressure sensors
#	- To take in the uplink commands
#	- Control the feedback of the pressure
# Inputs:
#	- PRessure and temperature sensors
#	- Motor, heaters, pressure system
#	- UPlink
# Outputs:
#	- State (6 states)
#	- Uplink (only for camera use)
# Created: 5/1/2018
# Modified: -/-
# Miura2 - main.py
#######################################################################
# Imports:
import threading
import time
import utility

#######################################################################
# Main Script:
utility_thread = threading.Thread(name = 'utility', target = utility.main)

utility_thread.start()


