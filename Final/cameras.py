##############################################################################
# Purpose:
#	- Includes functions of the three cameras
#	- 2 for pictures, one for video (quick shutter)
# Created: 6/1/2018
# Modified: 6/11/2018
# Miura 2 - cameras.py
# Lucas Zardini
##############################################################################
#imports
import os
import time
import threading

#time_delay = 0.5
temp = True
# main: thread function
def main(downlink_queue,running,stage):
	print('Camera thread initialized...')
	downlink_queue.put(['CM','BU', 0])
	while running:
		if stage == 1:
			pass
		elif stage == 2:
			if temp == True:
				stillCameras(1)
				temp == False
			else:
				stillCameras(2)

		elif stage == 3:
			stillCameras(2)

		elif stage == 4:
			stillCameras(2)

		elif stage == 5:
			stillCameras(2)

		elif stage == 6:
			stillCameras(2)

		#time.sleep(time_delay)




#still cameras (cameras 1 and 2)
def stillCameras(x):
	start = time.time()
	if x == 1:
		os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 cam1_' + str(start) + '.jpg')

		os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 -S 10 cam2_' + str(start) + '.jpg')

		os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 -S 10 cam3_' + str(start) + '.jpg')

	print(time.time()-start)
	elif x == 2:

		os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 cam1_' + str(start) + '.jpg')

		os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 cam3_' + str(start) + '.jpg')


	time.sleep(10)

#Fast shutter camera (Camera 2)
def videoCamera():
	start = time.time()

	os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 -S 10 cam2_' + str(start) + '.jpg')

	print(time.time()-start)

def singlePic():
	start = time.time()
	os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 test_' + str(start) + '.jpg')

