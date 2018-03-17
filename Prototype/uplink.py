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
import time

led_pin = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,GPIO.LOW)
GPIO.cleanup()

#LED ping when called
def led():
    GPIO.output(led_pin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led_pin,GPIO.LOW)
    GPIO.cleanup()

def main(ground):
    ground.flushInput() # Clears the serial communication channel before attempting to use it
    while True:
        print(ground.inWaiting())
	if ground.inWaiting(): # Reads uplink command
	    cmd = ground.read()  # gets command
	    print(cmd)
	    packet = hex(int.from_bytes((cmd), byteorder='big')) # Convert from hex into bytes
	    print(packet)
            if cmd == b"\xAA": # ping pi
                led()
                pass
            elif cmd == b"\xAB": # extend structure
                pass
            elif cmd == b"\xAC": # retract structure
                pass
            elif cmd == b"\xAD": # infinite motor loop
                pass
            else:
                print("invalid command")
        time.sleep(3)
                