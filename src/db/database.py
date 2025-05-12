from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime, ARRAY, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/case_study")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CampgroundDB(Base):
    __tablename__ = "campgrounds"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    region_name = Column(String)
    administrative_area = Column(String, nullable=True)
    nearest_city_name = Column(String, nullable=True)
    accommodation_type_names = Column(ARRAY(String))
    bookable = Column(Boolean, default=False)
    camper_types = Column(ARRAY(String))
    operator = Column(String, nullable=True)
    photo_url = Column(Text, nullable=True)
    photo_urls = Column(ARRAY(Text))
    photos_count = Column(Integer, default=0)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)
    slug = Column(String, nullable=True)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)
    availability_updated_at = Column(DateTime, nullable=True)

# Veritabanı tablolarını oluşturmak için
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
