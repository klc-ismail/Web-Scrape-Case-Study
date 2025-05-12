"""
Main entrypoint for The Dyrt web scraper case study.

Usage:
    The scraper can be run directly (`python main.py`) or via Docker Compose (`docker compose up`).

If you have any questions in mind you can connect to me directly via info@smart-maple.com
"""

from src.scraper import fetch_bbox_data, fetch_all_us_bboxes
from src.db.database import SessionLocal
from src.save_to_db import save_campgrounds
import time


if __name__ == "__main__":
    print("Scraping baslatildi")
    bboxes = fetch_all_us_bboxes()

    total_scraped = 0
    for i, bbox in enumerate(bboxes, start=1):
        print(f"🔍 {i}/{len(bboxes)} bbox: {bbox}")
        try:
            campgrounds = fetch_bbox_data(bbox)
            total_scraped += len(campgrounds)

            if campgrounds:
                with SessionLocal() as session:
                    save_campgrounds(session, campgrounds)

        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)  

    print(f"Toplam cekilen kamp alani: {total_scraped}")
