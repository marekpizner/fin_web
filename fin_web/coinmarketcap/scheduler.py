from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .downloader import start

def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start, 'interval', minutes=20)
    scheduler.start()