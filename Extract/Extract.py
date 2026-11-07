import ee

from ._extract_s1 import extract_Sentinel1
from ._extract_s2 import extract_Sentinel2


def extract(aoi: ee.Geometry, start_date: str, end_date: str, cloudy_pixel: int = 100) -> dict:
    """
    Extract phase: load the Sentinel-2 and Sentinel-1 collections for the AOI and date range.

    Parameters:
    - aoi (ee.Geometry): Area of interest.
    - start_date (str): Start date, 'YYYY-MM-DD' (inclusive).
    - end_date (str): End date, 'YYYY-MM-DD' (exclusive).
    - cloudy_pixel (int): Maximum CLOUDY_PIXEL_PERCENTAGE for Sentinel-2 scenes.

    Returns:
    - dict: {"Sentinel2": ee.ImageCollection, "Sentinel1": ee.ImageCollection}

    Raises:
    - ValueError: If either collection is empty.
    """
    print("Extracting Sentinel-2 data...")
    sentinel2_collection = extract_Sentinel2(aoi, start_date, end_date, cloudy_pixel)
    print(f"Extracted {sentinel2_collection.size().getInfo()} Sentinel-2 images.")

    print("Extracting Sentinel-1 data...")
    sentinel1_collection = extract_Sentinel1(aoi, start_date, end_date)
    print(f"Extracted {sentinel1_collection.size().getInfo()} Sentinel-1 images.")

    return {
        "Sentinel2": sentinel2_collection,
        "Sentinel1": sentinel1_collection,
    }
