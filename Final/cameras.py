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

# main: thread function
def main(downlink_queue,camera_queue):
	print('Camera thread initialized...')
	downlink_queue.put(['CM','BU', 0])
	last_pic = time.time()
	while True:
		current_time = time.time()

		if current_time - last_pic >= 5:
			takePicture()
			last_pic = current_time

		if not camera_queue.empty():
			command = camera_queue.get()
			if command == 'takeVideo':
				takeVideo()
			elif command == 'takePicture':
				takePicture()
		time.sleep(0.1)


#still cameras (cameras 1 and 3)
def takePicture():
	start = time.time()
	os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 pics/cam1_{}.jpg'.format(start))
	os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 -S 10 pics/cam3_{}.jpg'.format(start))

#Fast shutter camera (Camera 2)
def takeVideo():
	start = time.time()
	num_frames = 60
	duration = 10
	counter = 0
	while counter < num_frames:
		if counter == 0:
			os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 -S 10 pics/cam2_{}_{}.jpg'.format(start,counter))
		else:
			os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 pics/cam2_{}_{}.jpg'.format(start,counter))
		time.sleep(duration/num_frames)
