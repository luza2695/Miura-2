##################################################################
# Miura 2: Camera Functions (cameras.py)
# Created: 3/13/2018
# Modified: 6/10/2018
# Purpose: Functions to take pictures and videos
##################################################################
import os
import time

# still cameras (cameras 0 and 2)
def takePicture(data_directory):
	os.system('fswebcam -i 0 -d /dev/video0 -b -r 1024x768 -S 10 {}/cam0_{}.jpg'.format(data_directory,time.time()))
	os.system('fswebcam -i 0 -d /dev/video2 -b -r 1024x768 -S 10 {}/cam2_{}.jpg'.format(data_directory,time.time()))

# fast shutter camera (Camera 1)
def takeVideo(data_directory):
	start = time.time()
	frames = 60
	duration = 60
	counter = 0
	while counter < frames:
		if counter == 0:
			os.system('fswebcam -i 0 -d /dev/video1 -b -r 1024x768 -S 10 {}/cam1_{}_{}.jpg'.format(data_directory,start,counter))
		else:
			os.system('fswebcam -i 0 -d /dev/video1 -b -r 1024x768 -S 10 {}/cam1_{}_{}.jpg'.format(data_directory,start,counter))
		counter += 1
		time.sleep(duration/frames)
