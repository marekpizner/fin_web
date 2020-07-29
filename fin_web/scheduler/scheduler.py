from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .downloader_coinmarketcap import start as start_coinmarket
from .downloader_quandl import start as start_quandl


def run_now():
    start_quandl()


def scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(start_coinmarket, 'interval', minutes=2)
    scheduler.add_job(start_quandl, 'interval', minutes=20)
    scheduler.start()
