##################################################################
# Purpose: Controls/tests the outside luminati lights
# Created: 6/5/2018
# Modified: -/-/-
# Miura2 - lights.py
##################################################################
# Imports
import spidev
import time
import smbus
##################################################################
#variables for SPI
# address = 0xE0
# configbyte = 0x1c
# bus = smbus.SMBus(1)
# bus.write_byte(address,configbyte)

spi = spidev.SpiDev()
spi.open(0,0)


#Create LED array by sending this function num_LEDs
def set_LED_quantity(num_LEDs):
    global NUM_LEDs
    NUM_LEDs = num_LEDs
    global LED_array
    LED_array = [[0,0,0,0]] * NUM_LEDs

#Puts LED(num) parameters into LED_array
#Red, Green and Blue (r,g,b) values must be between
#0-255. Brightness must be between 0 and 31.
def set_LED(num, r, g, b, brightness):
    if (brightness > 31) | (brightness < 0):
        brightness = 15
    if (r > 255) | (r < 0):
        r = 100
    if (g > 255) | (g < 0):
        g = 100
    if (b > 255) | (b < 0):
        b = 100

    LED_array[num] = [r, g, b, brightness | 0xE0]

#These 4 bytes have to be written at the start and
#end of each data frame when writing to the LEDs
def _start_end_frame():
    for x in range (4):
            spi.xfer2([0x00])

#Write data to the LEDs
def WriteLEDs():
    _start_end_frame()
    for LED in LED_array:
        r, g, b, brightness = LED
        spi.xfer2([brightness])
        spi.xfer2([b])
        spi.xfer2([g])
        spi.xfer2([r])

    _start_end_frame()


#number of LEDs
set_LED_quantity(8)


#Delay
delay = 0.15

#brightness: 0-31
brightness = 15

while True:
    set_LED(0,25,25,25,brightness)

# try:
#     while True:

#         for y in range (5):

#             #center, white
#             set_LED(0,25,25,25,brightness)

#             #inner ring, red
#             for x in range (7):
#                 set_LED(x+1,25,0,0,brightness)

#             #outer ring, white
#             for x in range (12):
#                 set_LED(x+8,25,25,25,brightness)

#             #Write to the LEDs and wait
#             WriteLEDs()
#             time.sleep(wait)

#             #center, red
#             set_LED(0,25,0,0,brightness)

#             #inner ring, white
#             for x in range (7):
#                 set_LED(x+1,25,25,25,brightness)

#             #outer ring, red
#             for x in range (12):
#                 set_LED(x+8,25,0,0,brightness)

#             #Write to the LEDs and wait                               
#             WriteLEDs()
#             time.sleep(wait)

#         for y in range (5):

#             #center, yellow
#             set_LED(0,25,25,0,brightness)

#             #inner ring, blue
#             for x in range (7):
#                 set_LED(x+1,0,0,25,brightness)

#             #outer ring, yellow
#             for x in range (12):
#                 set_LED(x+8,25,25,0,brightness)

#             #Write to the LEDs and wait
#             WriteLEDs()
#             time.sleep(wait)

#             #center, blue
#             set_LED(0,0,0,25,brightness)

#             #inner ring, yellow
#             for x in range (7):
#                 set_LED(x+1,25,25,0,brightness)

#             #outer ring, blue
#             for x in range (12):
#                 set_LED(x+8,0,0,25,brightness)

#             #Write to the LEDs and wait                           
#             WriteLEDs()
#             time.sleep(wait)

# except KeyboardInterrupt:
#     pass






