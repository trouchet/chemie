# Description: This file is used to set up the scheduler for the application.
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.tasks.print_task import print_statement

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Test task: Add the scheduled task with a five-second interval
interval_1 = IntervalTrigger(seconds=5)
scheduler.add_job(print_statement, trigger=interval_1)