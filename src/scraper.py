import httpx
from typing import List
from pydantic import ValidationError
from src.models.campground import Campground
from tenacity import retry, stop_after_attempt, wait_fixed

API_URL = "https://thedyrt.com/api/v6/locations/search-results"

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_bbox_data(bbox: List[float], page: int = 1) -> List[Campground]:
    params = {
        "filter[search][bbox]": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        "filter[search][drive_time]": "any",
        "filter[search][air_quality]": "any",
        "filter[search][electric_amperage]": "any",
        "filter[search][max_vehicle_length]": "any",
        "filter[search][price]": "any",
        "filter[search][rating]": "any",
        "sort": "recommended",
        "page[number]": page,
        "page[size]": 500
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])

        campgrounds = []
        for item in data:
            try:
                attributes = item["attributes"]
                campground_data = {
                    **attributes,
                    "id": item["id"],
                    "type": item["type"],
                    "links": item["links"]
                }
                cg = Campground(**campground_data)
                campgrounds.append(cg)
            except ValidationError as e:
                print(f"❌ Validation error: {e}")

        return campgrounds

def fetch_all_us_bboxes() -> List[List[float]]:
    import itertools

    def frange(start, stop, step):
        while start < stop:
            yield round(start, 6)
            start += step

    USA_BBOX = [-125, 24, -66.5, 49.5]
    STEP = 1.0

    lons = list(frange(USA_BBOX[0], USA_BBOX[2], STEP))
    lats = list(frange(USA_BBOX[1], USA_BBOX[3], STEP))

    bbox_list = []
    for lon, lat in itertools.product(lons, lats):
        bbox = [lon, lat, lon + STEP, lat + STEP]
        bbox_list.append(bbox)

    return bbox_list
