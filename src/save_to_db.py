from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from src.models.campground import Campground
from src.db.database import CampgroundDB

def save_campgrounds(session: Session, campgrounds: List[Campground]):
    for cg in campgrounds:
        existing = session.get(CampgroundDB, cg.id)
        if existing:
            for field, value in cg.model_dump().items():
                setattr(existing, field, value)
        else:
            db_entry = CampgroundDB(**cg.model_dump())
            session.add(db_entry)

    try:
        session.commit()
        print(f"✅ {len(campgrounds)} kamp alanlari basariyla kaydedildi.")
    except IntegrityError as e:
        session.rollback()
        print(f"Error: {e}")
