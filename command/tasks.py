from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime

@periodic_task(run_every=(crontab(minute='*/5')), name="lock_picks", ignore_result=True)
def lock_picks():
    # do something
    print("The task ran at: " + datetime.now())