from apscheduler.schedulers.background import BackgroundScheduler
from backend.config import settings

scheduler = BackgroundScheduler()


def _reminder_job():
    """Job runs at configured times. Frontend polls /api/settings/reminder/status to show popup."""
    pass


def start_scheduler():
    if not scheduler.running:
        hour, minute = settings.reminder_time.split(":")
        scheduler.add_job(
            _reminder_job,
            "cron",
            hour=int(hour),
            minute=int(minute),
            id="daily_reminder",
        )
        scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
