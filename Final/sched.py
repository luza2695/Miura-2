##############################################################################



##############################################################################
import sched
import time

#Scheduler for stage 1
sched_stage1 = sched.scheduler(time.time, time.sleep)
def schedulerStage1(name):
	print("EVENT:", time.time(), name)
print("start", time.time(), name)
now = time.time()
scheduler.enter(1,1,schedulerStage1
