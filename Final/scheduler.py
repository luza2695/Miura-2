##############################################################################



##############################################################################
import sched
import time

#Scheduler for stage 1
sched_stage1 = sched.scheduler(time.time, time.sleep)
def schedulerStage1():
	now = time.time()
	elapsed = int(now-start)
	print("EVENT", time.time())

start = time.time()
print("START", start)
stage = 2
sched_stage1.enter(stage == 1,1,schedulerStage1, ())

sched_stage1.run()
