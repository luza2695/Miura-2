##################################################################
#Purpose:
#   - Accept uplink commands
#Created: 3/13/2018
#Modified: -/-
#Miura 2: Uplink Code (uplink.py)
#Project: Miura 2
##################################################################
#   -- Key Information --

#   -- Imports & Housing Keeping --
import subprocess
import RPi.GPIO as GPIO

led_pin = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,False)

def main(ground, motor_cmd):
    led_on = False
    ground.flushInput() # Clears the serial communication channel before attempting to use it
    while True:
	if led_on:
	    GPIO.output(led_pin,True)
	    led_on = False
	elif not led_on:
	    GPIO.output(led_pin,False)
	if ground.inWaiting(): # Reads uplink command
            led_on = True
	    cmd = ground.read()  # gets command
	    print(cmd)
	    packet = hex(int.from_bytes((cmd), byteorder='big')) # Convert from hex into bytes
	    print(packet)
            if cmd == b"xAA": # ping pi
                pass
            elif cmd == b"xAB": # extend structure
                pass
            elif cmd == b"xAC": # retract structure
                pass
            elif cmd == b"xAD": # infinite motor loop
                pass
            else:
                print("invalid command")
                