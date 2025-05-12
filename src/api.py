from fastapi import FastAPI
from src.scraper import fetch_all_us_bboxes, fetch_bbox_data
from src.db.database import SessionLocal
from src.save_to_db import save_campgrounds
from src.scheduler import start_scheduler
import time

app = FastAPI()

@app.on_event("startup")
def start_background_scheduler():
    start_scheduler()

@app.get("/ping")
def ping():
    return {"message": "API is running."}

@app.post("/run-scraper")
def run_scraper():
    bboxes = fetch_all_us_bboxes()
    total_scraped = 0

    for bbox in bboxes:
        try:
            campgrounds = fetch_bbox_data(bbox)
            total_scraped += len(campgrounds)

            if campgrounds:
                with SessionLocal() as session:
                    save_campgrounds(session, campgrounds)
        except Exception as e:
            return {"status": "error", "detail": str(e)}
        time.sleep(1)

    return {"status": "success", "total": total_scraped}
