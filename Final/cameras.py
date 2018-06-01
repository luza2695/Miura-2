##############################################################################
# Purpose:
#	- Includes functions of the three cameras
#	- 2 for pictures, one for video (quick shutter)
# Created: 6/1/2018
# Modified: -/-
# Miura 2 - cameras.py
# Lucas Zardini
##############################################################################
#imports
import os
import time

#still cameras (cameras 1 and 2)
def stillCameras(logic):
	while logic:
		start = time.time()

		os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 test1.jpg')

		os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 -S 10 test2.jpg')

		print(time.time()-start)

		time.sleep(2)
#Fast shutter camera (Camera 2)
def videoCamera(logic):
	while logic:
		start = time.time()

		os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 -S 10 test1.jpg')

		print(time.time()-start)

