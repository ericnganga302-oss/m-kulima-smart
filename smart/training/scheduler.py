from apscheduler.schedulers.background import BackgroundScheduler
from smart.training.retrain import retrain_growth_model

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        retrain_growth_model,
        trigger="interval",
        hours=24,
        id="daily_retrain",
        replace_existing=True
    )
    scheduler.start()
