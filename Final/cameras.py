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
def stillCameras():
	start = time.time()

	os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 cam1_' + str(start) + '.jpg')

	os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 -S 10 cam3_'+ str(start) + '.jpg')

	print(time.time()-start)

	time.sleep(2)
#Fast shutter camera (Camera 2)
def videoCamera():
	start = time.time()

	os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 -S 10 cam2_' + str(start) + '.jpg')

	print(time.time()-start)

def singlePic():
	start = time.time()
	os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 test_' + str(start) + '.jpg')


