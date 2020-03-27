from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .downloader_coinmarketcap import start as start_coinmarket
from .downloader_quandl import start as start_quandl


def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_coinmarket, 'interval', minutes=24 * 60)
    scheduler.add_job(start_quandl, 'interval', minutes=1)
    scheduler.start()
