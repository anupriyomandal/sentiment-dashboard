from apscheduler.schedulers.background import BackgroundScheduler
from backend.reddit_scraper import scrape_reddit_data
import logging

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def start_workers():
    logger.info("Starting background scheduler...")
    # Run once immediately to populate data (mock or real)
    try:
        scrape_reddit_data()
    except Exception as e:
        logger.error(f"Initial scrape failed: {e}")
        
    # Run every hour
    scheduler.add_job(scrape_reddit_data, 'interval', hours=1, id='reddit_scraper_job', replace_existing=True)
    scheduler.start()
