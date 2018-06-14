##################################################################
# Miura 2: Uplink Code (uplink.py)
# Created: 3/13/2018
# Modified: 6/7/2018
# Purpose: Accept uplink commands
##################################################################

import time
import serial
import sys
import motor
import solenoid
import queue
#import heater
import cameras
from helpers import changeStage

# sets current pi usb port
current_port = '/dev/ttyUSB0'

# Create serial object
serial = serial.Serial(port=current_port,
            baudrate=4800,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

def main(serial, downlink_queue, data_directory, manual, stage, stage_start_time, solenoid_1_enabled, solenoid_2_enabled):
    if serial.inWaiting(): # reads uplink command
        #heading = serial.read() # start of heading
        #start = serial.read() # start of text
        target = serial.read()
        command = serial.read()
        #end = serial.read() # end of text
        #cr_ = serial.read() # carriage return
        #lf_ = serial.read() # line feed
        downlink_queue.put(['UP','RE',target+command])
        if target == b'\x01':

            if command == b'\x01': # ping pi
                commandTime = time.strftime('%b %m %G %H:%M:%S')
                print('Ping Command Recieved: {}\n'.format(commandTime))
                pass

            elif command == b'\x02': # manual mode
                #Manual mode ON
                manual = True
                downlink_queue.put(['MA','MN',1])

            elif command == b'\x03': # continue automation mode
                # Manual mode OFF
                manual = False
                downlink_queue.put(['MA','MN',0])

            elif command == b'\x04': # restart automation mode
                #Manual mode OFF
                manual = False
                stage, stage_start_time = changeStage(2)
                downlink_queue.put(['MA','AU',1])

            elif command == b'\x05': # retract motor
                motor.main()
                downlink_queue.put(['MO','RE',1])

            elif command == b'\x06': # take video
                cameras.takeVideo(data_directory)
                downlink_queue.put(['CA','VI',1])

            elif command == b'\x07': # reboot pi
                subprocess.Popen('sudo reboot', shell=True)
                downlink_queue.put(['MA','RE',0])

            else:
                print('invalid command')

        elif target == b'\x02': # manual pressure system control

            if command == b'\x01': # open pressurization valve 1
                print('Opening Pressurize Valve 1')
                solenoid.openPressurize(1)
                downlink_queue.put(['SO','V1','OP'])

            elif command == b'\x02': # close pressurization valve 1
                print('Closing Pressurize Valve 1')
                solenoid.closePressurize(1)
                downlink_queue.put(['SO','V1','CL'])

            if command == b'\x03': # open pressurization valve 2
                print('Opening Pressurize Valve 2')
                solenoid.openPressurize(2)
                downlink_queue.put(['SO','V2','OP'])

            elif command == b'\x04': # close pressurization valve 2
                print('Closing Pressurize Valve 2')
                solenoid.closePressurize(2)
                downlink_queue.put(['SO','V2','CL'])

            elif command == b'\x05': # open exhaust valve
                print('Opening Exhaust Valve')
                solenoid.openExhaust()
                downlink_queue.put(['SO','EX','OP'])

            elif command == b'\x06': # close exhaust valve
                print('Closing Exhaust Valve')
                solenoid.closeExhaust()
                downlink_queue.put(['SO','EX','CL'])

            else:
                print('invalid command')

        elif target == b'\x03': # pressure system enabling control

            if command == b'\x01': # disable system 1
                solenoid_1_enabled = False
                downlink_queue.put(['SO','V1','DI'])

            elif command == b'\x02': # enable system 1
                solenoid_1_enabled = True
                downlink_queue.put(['SO','V1','EN'])

            elif command == b'\x03': # disable system 2
                solenoid_2_enabled = False
                downlink_queue.put(['SO','V2','DI'])

            elif command == b'\x04': # enable system 2
                solenoid_2_enabled = True
                downlink_queue.put(['SO','V2','EN'])

            else:
                print('invalid command')

        elif target == b'\x04': # heater system control

            if command == b'\x01': # turn on solenoid heaters
                #heater.solenoid_heater(True)
                downlink_queue.put(['HE','SO',1])

            elif command == b'\x02': # turn off solenoid heaters
                #heater.solenoid_heater(False)
                downlink_queue.put(['HE','SO',0])

            elif command == b'\x03': # turn on payload heaters
                #heater.payload_heater(True)
                downlink_queue.put(['HE','PA',1])

            elif command == b'\x04': # turn off payload heaters
                #heater.payload_heater(False)
                downlink_queue.put(['HE','PA',0])

            elif command == b'\x05': # turn on regulator heaters
                #heater.regulator_heater(True)
                downlink_queue.put(['HE','RG',1])

            elif command == b'\x06': # turn off regulator heaters
                #heater.regulator_heater(False)
                downlink_queue.put(['HE','RG',0])

            else:
                print('invalid command')

        else:
            print('invalid target')

    return manual, stage, stage_start_time, solenoid_1_enabled, solenoid_2_enabled

