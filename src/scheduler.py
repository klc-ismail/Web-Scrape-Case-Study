from apscheduler.schedulers.background import BackgroundScheduler
from src.scraper import fetch_all_us_bboxes, fetch_bbox_data
from src.db.database import SessionLocal
from src.save_to_db import save_campgrounds
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scheduled_scrape():
    logger.info("ABD kamp alanlari veri cekme islemi basladi.")
    bboxes = fetch_all_us_bboxes()
    total_scraped = 0

    for i, bbox in enumerate(bboxes, start=1):
        logger.info(f"🔍 {i}/{len(bboxes)} bbox: {bbox}")
        try:
            campgrounds = fetch_bbox_data(bbox)
            total_scraped += len(campgrounds)

            if campgrounds:
                with SessionLocal() as session:
                    save_campgrounds(session, campgrounds)

        except Exception as e:
            logger.error(f"❌ Hata oluştu: {e}")
        time.sleep(1)

    logger.info(f"İslem tamamlandi. Toplam kamp alani: {total_scraped}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_scrape, 'interval', hours=3)
    scheduler.start()
    logger.info("Zamanlayici basladi (her 3 saatte bir calisacak)")
