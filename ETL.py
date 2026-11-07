import ee

from Extract.Extract import extract
from Transform.Transform import transform
from Load.Load import load


def gee(aoi: ee.Geometry,
        start_date: str,
        end_date: str,
        cloudy_pixel: int,
        interval: int,
        name_file: str,
        name_folder: str,
        scale: int = 10,
        wait: bool = True) -> ee.batch.Task:
    """
    Run the full ETL pipeline: Extract -> Transform -> Load.

    Parameters:
    - aoi (ee.Geometry): Area of interest.
    - start_date (str): Start date, 'YYYY-MM-DD' (inclusive).
    - end_date (str): End date, 'YYYY-MM-DD' (exclusive).
    - cloudy_pixel (int): Maximum CLOUDY_PIXEL_PERCENTAGE for Sentinel-2 scenes (0-100).
    - interval (int): Length of each aggregation interval in days.
    - name_file (str): Output file name in Google Drive.
    - name_folder (str): Output folder in Google Drive.
    - scale (int): Export pixel size in metres.
    - wait (bool): Block until the export finishes.

    Returns:
    - ee.batch.Task: The export task.
    """
    # 1. Extract
    collections = extract(aoi, start_date, end_date, cloudy_pixel)
    print("Extracted Sentinel-1 and Sentinel-2 data.")

    # 2. Transform
    image = transform(aoi, start_date, end_date, interval,
                      collections["Sentinel2"], collections["Sentinel1"])
    print("Transformed Sentinel-1 and Sentinel-2 data.")

    # 3. Load
    return load(image, aoi, name_file, name_folder, scale=scale, wait=wait)
