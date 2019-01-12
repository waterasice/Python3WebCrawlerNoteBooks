from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Timer

import sched
def timer(n):
    while True:
        print(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
        time.sleep(n)

#timer(5)
def printtime(inc):
    print(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
    t = Timer(inc,printtime,(inc,))
    t.start()
#printtime(5)

schedule = sched.scheduler(time.time,time.sleep)

def pritime(inc):
    print(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
    schedule.enter(inc,0,pritime,(inc,))

def main(inc=60):
    schedule.enter(0,0,pritime,(inc,))
    schedule.run()
#main()

def job():
    print(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
scheduler = BlockingScheduler()
scheduler.add_job(job,'cron',day_of_week='1-6',hour=14,minute=59)
scheduler.start()
