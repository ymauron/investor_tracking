import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def run_crawl_job():
    from app.database import SessionLocal
    from app.services.crawler import crawl_all_feeds
    from app.services.matcher import clear_cache

    clear_cache()
    db = SessionLocal()
    try:
        stats = crawl_all_feeds(db)
        logger.info(f"Scheduled crawl complete: {stats}")
    except Exception:
        logger.exception("Scheduled crawl failed")
    finally:
        db.close()


def start_scheduler():
    if not settings.crawl_enabled:
        logger.info("Crawl scheduler disabled via config")
        return

    scheduler.add_job(
        run_crawl_job,
        trigger=CronTrigger(
            hour=settings.crawl_schedule_hour,
            minute=settings.crawl_schedule_minute,
        ),
        id="daily_rss_crawl",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        f"Crawl scheduler started: daily at {settings.crawl_schedule_hour:02d}:{settings.crawl_schedule_minute:02d}"
    )


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Crawl scheduler stopped")
