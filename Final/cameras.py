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
	os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 cam1_' + str(start) + '.jpg')
	os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 -S 10 cam3_' + str(start) + '.jpg')

#Fast shutter camera (Camera 2)
def takeVideo():
	os.system('ffmpeg -t 120 -f v4l2 -framerate 25 -video_size 640x80 -i /dev/video1 -t 300 output.mkv')

