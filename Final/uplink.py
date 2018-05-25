##################################################################
#Purpose:
#   - Accept uplink commands
#Created: 3/13/2018
#Modified: -/-
#Miura 2: Uplink Code (uplink.py)
#Project: Miura 2
##################################################################
#   -- Key Information --
#!/usr/bin/python
#   -- Imports & Housing Keeping --
import subprocess
import RPi.GPIO as GPIO
import time
import serial
import sys
sys.path.append('../')
#from Camera import cameratest
#import examples.StepperTest


led_pin = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,GPIO.LOW)
GPIO.cleanup()

# sets current pi usb port
current_port = "/dev/ttyUSB0"

# Create serial object
ground = serial.Serial(port=current_port,
            baudrate=4800,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)


#LED ping when called
def led():
    GPIO.output(led_pin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led_pin,GPIO.LOW)
    GPIO.cleanup()

def main(ground):
    ground.flushInput() # Clears the serial communication channel before attempting to use it
    while True:
        #print(ground.inWaiting())
        if ground.inWaiting(): # Reads uplink command
            cmd = ground.read()  # gets command
            packet = hex(int.from_bytes((cmd), byteorder='big')) # Convert from hex into bytes
            print(packet)
            if cmd == b"\x01": # ping pi
                cmdTime = time.asctime(time.localtime(time.time()))
                ground.write(bytes(5))
                #print(bytes(5))
                #print("Command Recieved :")#, cmdTime)
                pass
            elif cmd == b"\x02": # demo motor
                #StepperTest
            elif cmd == b"\x0C":
             	#cameratest.main()
                cmd = bytes('Nice picture!', 'utf-8')
                testDownlink.downlink(cmd)
            else:
                print("invalid command")
        time.sleep(1)
                
main(ground)
