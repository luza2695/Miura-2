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

#still cameras (cameras 1 and 3)
def takePicture(data_directory):
	start = time.time()
	os.system('fswebcam -i 0 -d /dev/video0 -b -r 1024x768 -S 10 {}/cam0_{}.jpg'.format(data_directory,start))
	os.system('fswebcam -i 0 -d /dev/video2 -b -r 1024x768 -S 10 {}/cam2_{}.jpg'.format(data_directory,start))

#Fast shutter camera (Camera 2)
def takeVideo(data_directory):
	start = time.time()
	frames = 60
	duration = 10
	counter = 0
	while counter < num_frames:
		if counter == 0:
			os.system('fswebcam -i 0 -d /dev/video1 -b -r 1024x768 -S 10 {}/cam1_{}_{}.jpg'.format(data_directory,start,counter))
		else:
			os.system('fswebcam -i 0 -d /dev/video1 -b -r 1024x768 -S 10 {}/cam1_{}_{}.jpg'.format(data_directory,start,counter))
		counter += 1
		time.sleep(duration/frames)
