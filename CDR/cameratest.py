import os
import time

start = time.time()

os.system('fswebcam -q -i 0 -d /dev/video0 -r 1024x768 -S 10 test1.jpg')


print(time.time()-start)
